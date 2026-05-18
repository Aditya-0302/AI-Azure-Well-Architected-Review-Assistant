"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { scoreTrend } from "@/data/platform";

export function ScoreTrendChart() {
  return (
    <div className="h-[280px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={scoreTrend} margin={{ left: 0, right: 12, top: 8, bottom: 0 }}>
          <defs>
            <linearGradient id="securityFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.35} />
              <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="operationsFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(var(--success))" stopOpacity={0.25} />
              <stop offset="95%" stopColor="hsl(var(--success))" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis dataKey="month" tickLine={false} axisLine={false} fontSize={12} />
          <YAxis tickLine={false} axisLine={false} fontSize={12} domain={[40, 100]} />
          <Tooltip
            contentStyle={{
              background: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: 8
            }}
          />
          <Area type="monotone" dataKey="Security" stroke="hsl(var(--primary))" fill="url(#securityFill)" strokeWidth={2} />
          <Area type="monotone" dataKey="Operations" stroke="hsl(var(--success))" fill="url(#operationsFill)" strokeWidth={2} />
          <Area type="monotone" dataKey="Reliability" stroke="hsl(var(--warning))" fill="transparent" strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

