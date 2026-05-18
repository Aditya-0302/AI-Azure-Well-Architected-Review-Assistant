"use client";

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

const data = [
  { name: "Critical", value: 2, color: "hsl(var(--critical))" },
  { name: "High", value: 8, color: "hsl(var(--warning))" },
  { name: "Medium", value: 19, color: "hsl(var(--primary))" },
  { name: "Low", value: 31, color: "hsl(var(--success))" }
];

export function SeverityDistribution() {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" outerRadius={100} innerRadius={58} paddingAngle={3}>
            {data.map((entry) => (
              <Cell key={entry.name} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              background: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: 8
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

