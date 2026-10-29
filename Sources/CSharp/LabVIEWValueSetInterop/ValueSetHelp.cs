using System;
using System.Collections.Generic;
using Windows.Foundation.Collections; // Nécessite référence WinRT

namespace LabVIEWValueSetInterop
{
    public static class ValueSetHelper
    {
        /// <summary>
        /// Convertit un ValueSet en string[] (clé1, val1, clé2, val2, ...)
        /// </summary>
        public static string[] ToStringArray(ValueSet vs)
        {
            var result = new List<string>();
            if (vs != null)
            {
                foreach (var kv in vs)
                {
                    result.Add(kv.Key?.ToString() ?? "");
                    result.Add(kv.Value?.ToString() ?? "");
                }
            }
            return result.ToArray();
        }
    }
}
