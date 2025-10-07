# TimeWise Typography Guide

This document outlines the official font styles, sizes, weights, and usage standards for the TimeWise productivity app UI.

---

## 🅰️ Font Family

| Type     | Font Stack                                                 | Usage                        |
| -------- | ---------------------------------------------------------- | ---------------------------- |
| Primary  | `Inter, ui-sans-serif, system-ui, sans-serif`              | All body and interface text  |
| Fallback | `system-ui, -apple-system, BlinkMacSystemFont, sans-serif` | Backup if primary is missing |

*Make sure Inter is loaded via Google Fonts or included in your project setup.*

---

## 🔠 Font Sizes & Usage    

| Token      | Tailwind Class | Size       | Usage                                    |
| ---------- | -------------- | ---------- | ---------------------------------------- |
| Display    | `text-5xl`     | \~3rem     | Hero section titles                      |
| Heading XL | `text-4xl`     | \~2.25rem  | Section titles (e.g., Features, Reviews) |
| Heading L  | `text-3xl`     | \~1.875rem | Subsection headers                       |
| Heading M  | `text-2xl`     | \~1.5rem   | Modal headers, form titles               |
| Heading S  | `text-xl`      | \~1.25rem  | Card titles, small headers               |
| Body L     | `text-base`    | \~1rem     | Main body text                           |
| Body S     | `text-sm`      | \~0.875rem | Captions, notes                          |
| Label      | `text-xs`      | \~0.75rem  | Buttons, UI labels                       |

---

## 💪 Font Weights

| Token    | Tailwind Class  | Usage                         |
| -------- | --------------- | ----------------------------- |
| Bold     | `font-bold`     | Headings, important UI labels |
| Semibold | `font-semibold` | Subheadings, card titles      |
| Medium   | `font-medium`   | Labels, buttons               |
| Normal   | `font-normal`   | Regular body text             |
| Light    | `font-light`    | Subtext, muted information    |

---

## 🧑‍💻 UI Hierarchy Examples

### Hero Title

```tsx
<h1 className="text-5xl font-extrabold leading-tight">Master Your Time with TimeWise</h1>
```

### Section Header

```tsx
<h2 className="text-3xl font-bold text-center">Features</h2>
```

### Card Title

```tsx
<h3 className="text-xl font-semibold">Analytics Dashboard</h3>
```

### Body Text

```tsx
<p className="text-base text-gray-600 dark:text-gray-300">Track your goals and stay productive.</p>
```

---

## 📋 Accessibility Notes

* Maintain minimum contrast ratio of **4.5:1** for body text.
* Always use semantic tags (`<h1>` to `<h6>`, `<p>`, `<button>`, etc.).
* Avoid excessive font weight combinations.

---

For brand colors, see `brand.md`. For logo usage, see `logo.md`.
