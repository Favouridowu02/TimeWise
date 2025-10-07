# TimeWise Brand Color Scheme

This document defines the official color palette and usage guidelines for the TimeWise productivity app.

---

## 🎨 Primary Palette

| Color Name     | Hex       | Usage                            |
| -------------- | --------- | -------------------------------- |
| Timewise Blue  | `#2563EB` | Primary actions, buttons, links  |
| Timewise Light | `#DBEAFE` | Background highlights, hero bg   |
| Timewise Dark  | `#1E3A8A` | Dark theme accents, hover states |

## 🌑 Dark Mode Palette

| Color Name | Hex       | Usage                            |
| ---------- | --------- | -------------------------------- |
| Deep Gray  | `#111827` | Background                       |
| Soft Gray  | `#374151` | Card backgrounds, subtle borders |
| Light Text | `#F3F4F6` | Headings, high contrast text     |
| Muted Text | `#9CA3AF` | Secondary text                   |

## 🌟 Accent Colors

| Color Name    | Hex       | Usage                             |
| ------------- | --------- | --------------------------------- |
| Success Green | `#10B981` | Goal tracking, success indicators |
| Warning Amber | `#F59E0B` | Deadlines, important alerts       |
| Error Red     | `#EF4444` | Errors, failed actions            |

## ⚙️ Typography Color Use

* **Headings:** `#1F2937` (Dark), `#F3F4F6` (Light)
* **Body Text:** `#374151` (Dark), `#D1D5DB` (Light)
* **Links & CTAs:** Use **Timewise Blue** in both light and dark modes.

## 🧩 Tailwind Customization

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          blue: '#2563EB',
          light: '#DBEAFE',
          dark: '#1E3A8A',
          gray: {
            deep: '#111827',
            soft: '#374151',
            text: '#9CA3AF',
            lightText: '#F3F4F6',
          },
          success: '#10B981',
          warning: '#F59E0B',
          error: '#EF4444',
        },
      },
    },
  },
};
```

---

## ✅ Usage Guidelines

* Use **Timewise Blue** as the dominant brand color.
* Accent colors should be used sparingly to draw attention.
* Maintain accessibility contrast standards.
* Always test dark mode styling alongside light mode.

---

For logo and typography branding, refer to `logo.md` and `typography.md` files.
