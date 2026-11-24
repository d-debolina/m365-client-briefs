// CREW · WorkdayMath plug-in (Day 31)
// Sets crew_enddate from crew_startdate + crew_durationworkdays, skipping weekends and rows in crew_holiday.
// Register: Create and Update of crew_task, stage PreOperation (20), synchronous,
//           filtering attributes crew_startdate, crew_durationworkdays.
// Same rules as add_workdays() in engine/planning_engine.py, so the acceptance tests cover both.
using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Xrm.Sdk;
using Microsoft.Xrm.Sdk.Query;

namespace Crew.Plugins
{
    public sealed class WorkdayMath : IPlugin
    {
        public void Execute(IServiceProvider serviceProvider)
        {
            var context = (IPluginExecutionContext)serviceProvider.GetService(typeof(IPluginExecutionContext));
            var service = ((IOrganizationServiceFactory)serviceProvider.GetService(typeof(IOrganizationServiceFactory)))
                .CreateOrganizationService(context.UserId);

            var target = (Entity)context.InputParameters["Target"];
            context.PreEntityImages.TryGetValue("pre", out Entity pre);

            DateTime? start = target.Contains("crew_startdate") ? target.GetAttributeValue<DateTime?>("crew_startdate")
                                                                 : pre?.GetAttributeValue<DateTime?>("crew_startdate");
            int? days = target.Contains("crew_durationworkdays") ? target.GetAttributeValue<int?>("crew_durationworkdays")
                                                                  : pre?.GetAttributeValue<int?>("crew_durationworkdays");
            if (start == null || days == null) return;

            var holidays = new HashSet<DateTime>(service.RetrieveMultiple(new QueryExpression("crew_holiday")
                { ColumnSet = new ColumnSet("crew_date") }).Entities
                .Select(e => e.GetAttributeValue<DateTime>("crew_date").Date));

            target["crew_enddate"] = AddWorkdays(start.Value.Date, days.Value, holidays);
        }

        public static DateTime AddWorkdays(DateTime start, int days, ISet<DateTime> holidays)
        {
            var d = start;
            while (days > 0)
            {
                d = d.AddDays(1);
                if (d.DayOfWeek != DayOfWeek.Saturday && d.DayOfWeek != DayOfWeek.Sunday && !holidays.Contains(d)) days--;
            }
            return d;
        }
    }
}
