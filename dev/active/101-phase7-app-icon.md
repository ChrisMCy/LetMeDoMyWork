# Task 101: Create App Icon

## Phase
7 - Release Preparation

## Description
Design and implement the app icon.

## Steps
1. Design icon (512x512)
2. Generate all required sizes
3. Configure in Android

## Icon Requirements

### Design Guidelines
- Simple, recognizable shape
- Works at small sizes (48px)
- Follows Material Design guidelines
- No text (won't be readable)
- Represents email/follow-up concept

### Suggested Design
```
Concept: Email icon with clock/repeat element

Option A: Envelope with circular arrow
- Blue envelope base
- Small clock or refresh icon overlay
- Clean, professional look

Option B: Stylized "L" with email
- Letter "L" incorporating envelope
- Modern, minimal design

Option C: Email with checkmark trail
- Email icon with checkmarks
- Represents successful follow-ups
```

### Required Sizes (Android)
```
android/app/src/main/res/
├── mipmap-mdpi/ic_launcher.png      (48x48)
├── mipmap-hdpi/ic_launcher.png      (72x72)
├── mipmap-xhdpi/ic_launcher.png     (96x96)
├── mipmap-xxhdpi/ic_launcher.png    (144x144)
├── mipmap-xxxhdpi/ic_launcher.png   (192x192)
└── mipmap-anydpi-v26/
    └── ic_launcher.xml              (Adaptive icon)
```

### Adaptive Icon (Android 8.0+)
```xml
<!-- ic_launcher.xml -->
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
```

### Background Color
```xml
<!-- colors.xml -->
<resources>
    <color name="ic_launcher_background">#5C6BC0</color>
</resources>
```

## Tools for Generation
- Android Studio Image Asset Studio
- Online: https://romannurik.github.io/AndroidAssetStudio/
- Figma/Sketch for design

## Generation Steps
1. Create 512x512 PNG design
2. In Android Studio: File > New > Image Asset
3. Select "Launcher Icons (Adaptive and Legacy)"
4. Import your design
5. Preview on different shapes
6. Generate

## Acceptance Criteria
- [ ] Icon designed (512x512 master)
- [ ] All mipmap sizes generated
- [ ] Adaptive icon configured
- [ ] Icon displays correctly on device
- [ ] Works on different launcher shapes
- [ ] Professional appearance

## Dependencies
- None

## Parallel Work
Can run parallel with: Task 102, 103

## Estimated Effort
2-3 hours (design) + 30 min (implementation)
