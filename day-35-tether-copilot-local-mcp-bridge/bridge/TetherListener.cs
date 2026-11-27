// TETHER local bridge — UNTESTED SKETCH (not compiled in this repo). Shows the shape only.
// Runs as a Windows service next to the app. Dials OUT to Azure Relay (443), receives relayed HTTP
// requests, applies the same checks as scripts/tether_gate.py, then calls the app's own MCP server
// on http://127.0.0.1:<port>/mcp. NuGet: Microsoft.Azure.Relay
using Microsoft.Azure.Relay;
using System.Net;
using System.Text;

var ns   = Environment.GetEnvironmentVariable("TETHER_RELAY_NAMESPACE"); // e.g. tether-relay.servicebus.windows.net
var hc   = Environment.GetEnvironmentVariable("TETHER_HYBRID_CONNECTION"); // one per customer install
var key  = Environment.GetEnvironmentVariable("TETHER_LISTEN_KEY");        // Listen-only SAS key, stored with DPAPI in the real build
var local = new HttpClient { BaseAddress = new Uri("http://127.0.0.1:47800/"), Timeout = TimeSpan.FromSeconds(50) };

var tokens = TokenProvider.CreateSharedAccessSignatureTokenProvider("tether-listen", key);
var listener = new HybridConnectionListener(new Uri($"sb://{ns}/{hc}"), tokens);

listener.RequestHandler = async ctx =>
{
    // The relay only forwards requests signed with the Send key, which only APIM holds,
    // so x-tether-user was set by APIM from a validated Entra token.
    var user = ctx.Request.Headers["x-tether-user"];
    using var reader = new StreamReader(ctx.Request.InputStream, Encoding.UTF8);
    var body = await reader.ReadToEndAsync();          // JSON-RPC: initialize, tools/list, tools/call

    // 1. Gate (role filter on tools/list, workspace + path fences, two-step confirmation on writes)
    var decision = Gate.Check(user, body);              // port of scripts/tether_gate.py
    string reply = decision.Allowed
        ? await (await local.PostAsync("mcp", new StringContent(decision.ForwardBody, Encoding.UTF8, "application/json"))).Content.ReadAsStringAsync()
        : decision.JsonRpcReply;                         // denied / needs_confirmation as a normal tool result

    Audit.Write(user, body, decision);                   // local log + optional Event Log
    ctx.Response.StatusCode = HttpStatusCode.OK;
    ctx.Response.Headers["Content-Type"] = "application/json";   // JSON, not SSE: stay inside the relay's 60 s window
    var bytes = Encoding.UTF8.GetBytes(reply);
    await ctx.Response.OutputStream.WriteAsync(bytes);
    await ctx.Response.CloseAsync();
};

await listener.OpenAsync();
Console.WriteLine($"TETHER listening on {hc}. No inbound ports open.");
await Task.Delay(Timeout.Infinite);
