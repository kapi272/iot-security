# UI Context

## Theme

The visual language is an official, minimal, and technical workspace. It supports both light and dark modes, prioritizing absolute legibility for data-dense security logs, Suricata alerts, and topology configurations. Surfaces rely on subtle border separations rather than heavy shadows, and vivid state colors are reserved strictly for critical network alerts and interactive attack triggers.

## Colors

| Role | CSS Variable | Light Mode | Dark Mode |
| :--- | :--- | :--- | :--- |
| Page background | `--bg-base` | `#F8FAFC` | `#020617` |
| Panel surface | `--bg-surface` | `#FFFFFF` | `#0F172A` |
| Primary text | `--text-primary` | `#0F172A` | `#F8FAFC` |
| Muted text | `--text-muted` | `#64748B` | `#94A3B8` |
| Primary accent | `--accent-primary` | `#0284C7` | `#38BDF8` |
| Border outline | `--border-default` | `#E2E8F0` | `#1E293B` |
| AI / Anomaly | `--state-warning` | `#D97706` | `#FBBF24` |
| Threat (Attack) | `--state-error` | `#DC2626` | `#F87171` |
| Safe (Active) | `--state-success` | `#059669` | `#34D399` |

## Typography

| Role | Font Family | Variable |
| :--- | :--- | :--- |
| UI text | Inter | `--font-sans` |
| Code/mono | JetBrains Mono | `--font-mono` |

## Border Radius

| Context | Class |
| :--- | :--- |
| Inline / small UI | `rounded-sm` |
| Cards / panels | `rounded-md` |
| Modals / overlays | `rounded-lg` |

## Component Library

shadcn/ui on top of Tailwind CSS. Components live in `components/ui/`. Use the CLI to add new components rather than writing from scratch.

## Layout Patterns

- Grid Layouts: Fixed top navigation bar with a responsive CSS grid below to properly scale the embedded Kibana telemetry iframe.
- Action Surfaces: Fixed, left-aligned control sidebar separated by a default border for Mininet simulation parameters and attack trigger buttons.
- Terminal Output: Dark-mode backgrounds strictly enforced for raw subprocess logs (like Hydra or Nmap outputs) to preserve terminal authenticity regardless of the active page theme.

## Icons

Lucide React. Stroke-based icons only. Sizes: `h-4 w-4` for inline, `h-5 w-5` for buttons.