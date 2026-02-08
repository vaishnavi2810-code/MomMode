import type { ComponentType, ReactNode, SVGProps } from 'react'

type StatCardProps = {
  title: string
  value: ReactNode
  change?: ReactNode
  icon: ComponentType<SVGProps<SVGSVGElement>>
  accent?: 'primary' | 'success' | 'warning'
}

const accentStyles: Record<NonNullable<StatCardProps['accent']>, string> = {
  primary: 'bg-primary/10 text-primary ring-1 ring-primary/20',
  success: 'bg-success/10 text-success ring-1 ring-success/20',
  warning: 'bg-warning/10 text-warning ring-1 ring-warning/30',
}

const StatCard = ({ title, value, change, icon: Icon, accent = 'primary' }: StatCardProps) => {
  return (
    <div className="min-h-[140px] rounded-2xl border border-slate-200 bg-white p-5 shadow-soft transition hover:-translate-y-0.5 hover:shadow-[0_16px_35px_rgba(15,23,42,0.12)]">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">{title}</p>
          <div className="mt-2 flex flex-wrap items-baseline gap-2 text-3xl font-semibold text-slate-900">
            {value}
          </div>
        </div>
        <div className={`flex h-11 w-11 items-center justify-center rounded-2xl ${accentStyles[accent]} shadow-sm`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      {change ? <div className="mt-4 text-sm font-medium text-slate-500">{change}</div> : null}
    </div>
  )
}

export default StatCard
