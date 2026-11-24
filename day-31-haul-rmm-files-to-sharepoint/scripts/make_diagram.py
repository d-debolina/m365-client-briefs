"""Draws architecture.dot/.svg/.png for Day 31 HAUL with the series helpers in tools/diagrams.py."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
from diagrams import n, b, cluster, render

body = (
    n("rmm", b("RMM tool", "schedules the job · runs as SYSTEM<br/>reads exit codes 0–5"), "user")
    + cluster("pc", "Each client PC (Windows 10/11, Server 2016+)", "doc",
        n("src", b("C:\\Fabrikam\\PM", "top-level files only<br/>changed in the last 3 days"), "doc")
        + n("haul", b("Invoke-Haul.ps1", "hash check · locked-file safe<br/>retry + Retry-After · mutex"), "doc")
        + n("cert", b("Certificate", "LocalMachine\\My<br/>non-exportable key"), "doc")
        + n("state", b("state.json + haul.log", "C:\\ProgramData\\Haul"), "doc"))
    + cluster("entra", "Microsoft Entra ID", "azure",
        n("app", b("App registration", "certificate credential · no secret<br/>Lists.SelectedOperations.Selected"), "azure")
        + n("ca", b("Optional: Conditional Access", "for workload identities (Premium)<br/>sign-in logs · alerts"), "azure"))
    + cluster("m365", "SharePoint Online (MSP tenant)", "m365",
        n("mg", b("Microsoft Graph", "PUT …:/content (≤ 10 MiB)<br/>createUploadSession (bigger)"), "m365")
        + n("lib", b("Client drop-zone library", "app has <i>write</i> on this library only<br/>PM / &lt;COMPUTERNAME&gt; / file"), "m365"))
    + """  rmm -> haul [label="hourly"];
  src -> haul; haul -> state [style=dashed, label="remember hashes"];
  cert -> haul [label="signs PS256 assertion", style=dotted];
  haul -> app [label="client credentials"]; app -> haul [label="access token", style=dashed];
  app -> ca [style=dotted];
  haul -> mg [label="upload"]; mg -> lib;
  haul -> rmm [label="exit code + log", style=dashed];
"""
)

render("day-31-haul-rmm-files-to-sharepoint",
       "Day 31 · HAUL — Hash-checked, App-only, Unattended, Logged",
       "Files from many remote PCs to one SharePoint library, with a certificate instead of a password",
       body)
