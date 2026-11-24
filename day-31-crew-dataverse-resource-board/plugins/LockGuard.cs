// CREW · LockGuard plug-in (Day 31)
// Stops edits to a locked look-ahead task from ANY client: the model-driven app, Excel "Edit in Excel",
// Power Automate, the Web API or an import. Business rules and form scripts only run in the app; this runs in Dataverse.
//
// Register (Plug-in Registration tool):
//   Message Update, table crew_task, stage PreValidation (10), synchronous,
//     filtering attributes: crew_startdate, crew_durationworkdays, crew_assignedcrew, crew_projectid
//     pre-image alias "pre" with crew_projectid
//   Message Delete, table crew_task, stage PreValidation (10), synchronous, pre-image alias "pre"
// Unlock path: the Teams approval flow sets crew_project.crew_unlockeduntil; edits are allowed until that time.
// Fictional sample. Build against Microsoft.CrmSdk.CoreAssemblies (or the Dataverse plug-in template in PAC CLI).
using System;
using Microsoft.Xrm.Sdk;

namespace Crew.Plugins
{
    public sealed class LockGuard : IPlugin
    {
        public void Execute(IServiceProvider serviceProvider)
        {
            var context = (IPluginExecutionContext)serviceProvider.GetService(typeof(IPluginExecutionContext));
            var trace = (ITracingService)serviceProvider.GetService(typeof(ITracingService));
            var factory = (IOrganizationServiceFactory)serviceProvider.GetService(typeof(IOrganizationServiceFactory));
            var service = factory.CreateOrganizationService(null); // SYSTEM: read the lock even if the user can't see the project

            if (!context.PreEntityImages.TryGetValue("pre", out Entity pre) ||
                !pre.Contains("crew_projectid"))
            {
                trace.Trace("LockGuard: pre-image 'pre' with crew_projectid is missing. Check the step registration.");
                return;
            }

            var projectRef = pre.GetAttributeValue<EntityReference>("crew_projectid");
            var project = service.Retrieve("crew_project", projectRef.Id,
                new Microsoft.Xrm.Sdk.Query.ColumnSet("crew_planlocked", "crew_unlockeduntil", "crew_name"));

            bool locked = project.GetAttributeValue<bool>("crew_planlocked");
            var unlockedUntil = project.GetAttributeValue<DateTime?>("crew_unlockeduntil");
            bool unlockWindowOpen = unlockedUntil.HasValue && unlockedUntil.Value > DateTime.UtcNow;

            if (locked && !unlockWindowOpen)
            {
                trace.Trace($"LockGuard: blocked {context.MessageName} on task {context.PrimaryEntityId} by user {context.InitiatingUserId}");
                throw new InvalidPluginExecutionException(
                    $"The plan for '{project.GetAttributeValue<string>("crew_name")}' is locked. " +
                    "Ask for an unlock in Teams (Request unlock button) and try again after it's approved.");
            }
        }
    }
}
