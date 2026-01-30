# Task 087: Phase 4 Validation

## Phase
4 - Advanced Features (Validation)

## Description
Validate all Phase 4 deliverables.

## Steps
1. Test statistics calculations
2. Test template management
3. Test export/import round-trip

## Validation Checklist

### 1. Statistics Tests

#### Overall Stats
- [ ] Total TODOs count correct
- [ ] Active/Completed/Paused counts correct
- [ ] Total emails sent calculated correctly
- [ ] Average emails per TODO calculated
- [ ] This week stats use correct date range

#### Recipient Stats
- [ ] Grouped by email correctly
- [ ] Shows first/last name when available
- [ ] Email count per recipient correct
- [ ] Sorted by most emails

#### Heatmap
- [ ] Shows last 4 weeks
- [ ] Daily counts correct
- [ ] Color intensity matches activity
- [ ] Legend displayed

### 2. Template Management Tests

#### Display
- [ ] Tab bar switches between Subjects/Bodies
- [ ] Language toggle switches templates
- [ ] All templates displayed

#### Editing
- [ ] Add new template via FAB
- [ ] Edit existing template
- [ ] Delete template (with confirmation)
- [ ] Cannot delete last template

#### Reordering
- [ ] Drag handle visible
- [ ] Reorder works correctly
- [ ] Order persists after save

#### Persistence
- [ ] Save button saves changes
- [ ] Templates persist after app restart
- [ ] Correct templates shown in TODO creation

### 3. Export/Import Tests

#### Export
- [ ] Export to file works
- [ ] File saved to accessible location
- [ ] Share option works
- [ ] JSON format correct
- [ ] All data included (todos, settings, sent_emails)

#### Import
- [ ] File picker opens
- [ ] Invalid files rejected with message
- [ ] Preview shows correct counts
- [ ] Confirmation dialog appears
- [ ] Data replaced correctly
- [ ] Settings reloaded after import

#### Round-Trip Test
1. [ ] Create several TODOs
2. [ ] Send some emails
3. [ ] Modify settings
4. [ ] Export data
5. [ ] Clear app data / reinstall
6. [ ] Import backup
7. [ ] Verify all data restored:
   - [ ] All TODOs present
   - [ ] All sent emails present
   - [ ] Settings restored
   - [ ] Send counts correct

### 4. Integration

- [ ] Statistics accessible from main screen
- [ ] Template management accessible from settings
- [ ] Export/Import accessible from settings
- [ ] No crashes during any operation

## Bug Tracking

| # | Description | Severity | Status |
|---|-------------|----------|--------|
| 1 | | | |

## Acceptance Criteria
- [ ] All statistics calculate correctly
- [ ] Template management fully functional
- [ ] Export/Import round-trip successful
- [ ] No data loss

## Dependencies
- Task 080-086 (All Phase 4 tasks)

## Next Phase
Phase 5: Background Service & Notifications

## Estimated Effort
2-3 hours
