# Task 093: Phase 5 Validation

## Phase
5 - Background Service & Notifications (Validation)

## Description
Validate all Phase 5 deliverables - automatic email sending should work.

## Steps
1. Test notifications
2. Test background service
3. Test offline handling
4. Test 7-day inactivity

## Validation Checklist

### 1. Notification Tests

- [ ] Email sent notification appears
- [ ] Shows recipient name and subject
- [ ] Email failed notification shows error
- [ ] Inactivity notification works
- [ ] Pending sends notification shows count
- [ ] Tapping notification opens app
- [ ] Notifications can be dismissed

### 2. Background Service Tests

**Setup Test:**
- [ ] WorkManager initializes without error
- [ ] Periodic task registered

**Manual Test (Short Interval):**
1. [ ] Create TODO with next_send in 5 minutes
2. [ ] Close app completely
3. [ ] Wait for next_send time
4. [ ] Email should be sent
5. [ ] Notification should appear
6. [ ] Open app - UI should reflect sent email

**Failure Test:**
1. [ ] Configure invalid SMTP credentials
2. [ ] Create TODO with next_send in 5 minutes
3. [ ] Close app
4. [ ] Wait for trigger
5. [ ] Failure notification should appear
6. [ ] TODO should have error state

### 3. Offline Handling Tests

**Going Offline:**
- [ ] Enable airplane mode
- [ ] App shows offline banner
- [ ] Manual send shows error
- [ ] Scheduled sends marked as pending

**Coming Online:**
- [ ] Disable airplane mode
- [ ] Offline banner disappears
- [ ] Pending sends triggered
- [ ] Notifications for sent emails

### 4. 7-Day Inactivity Tests

**Simulation (DB Manipulation):**
1. [ ] Create several active TODOs
2. [ ] Manually set last_opened to 8 days ago in SharedPreferences
3. [ ] Force close and reopen app
4. [ ] Inactivity dialog should appear
5. [ ] Shows correct count of paused TODOs

**Resume All Test:**
- [ ] Click "Resume All"
- [ ] All TODOs resumed
- [ ] next_send_datetime recalculated
- [ ] Snackbar confirmation shown

**Keep Paused Test:**
- [ ] Click "Keep Paused"
- [ ] TODOs remain paused
- [ ] No snackbar shown
- [ ] Can manually resume from list

### 5. Battery & Performance Tests

- [ ] Background service respects battery saver
- [ ] No excessive battery drain
- [ ] App survives device restart
- [ ] Service restarts after reboot

### 6. Multi-Device Testing

Test on different Android versions:
- [ ] Android 10 (API 29)
- [ ] Android 12 (API 31)
- [ ] Android 13 (API 33)
- [ ] Android 14 (API 34)

Note any manufacturer-specific issues:
- Xiaomi: May require disable battery optimization
- Huawei: May require disable battery optimization
- Samsung: Generally works

## Known Issues to Document

Document any issues that require user action:
- Battery optimization whitelist instructions
- Manufacturer-specific settings
- Notification permissions

## Bug Tracking

| # | Description | Severity | Status |
|---|-------------|----------|--------|
| 1 | | | |

## Acceptance Criteria
- [ ] Emails send automatically in background
- [ ] Notifications work for all events
- [ ] Offline handling graceful
- [ ] 7-day inactivity flow works
- [ ] Survives device restart
- [ ] Works on Android 10-14

## Dependencies
- Task 088-092 (All Phase 5 tasks)

## Next Phase
Phase 6: Polish & Testing

## Estimated Effort
4-6 hours (including testing on multiple devices)
