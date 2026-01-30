# Task 082: Create Statistics Widgets

## Phase
4 - Advanced Features

## Description
Create reusable widgets for the statistics screen.

## Steps
1. Create `lib/presentation/screens/statistics/widgets/` directory
2. Implement StatCard
3. Implement RecipientList
4. Implement HeatmapChart

## Code Structure

### stat_card.dart
```dart
import 'package:flutter/material.dart';
import '../../../../core/theme/app_dimensions.dart';

class StatCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color color;
  final String? subtitle;

  const StatCard({
    super.key,
    required this.title,
    required this.value,
    required this.icon,
    required this.color,
    this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(AppDimensions.radiusLg),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  title,
                  style: TextStyle(
                    color: color,
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(
              color: color,
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),
          if (subtitle != null)
            Text(
              subtitle!,
              style: TextStyle(
                color: color.withOpacity(0.7),
                fontSize: 11,
              ),
            ),
        ],
      ),
    );
  }
}
```

### recipient_list.dart
```dart
import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../domain/usecases/statistics/get_recipient_stats_usecase.dart';

class RecipientList extends StatelessWidget {
  final List<RecipientStats> recipients;

  const RecipientList({
    super.key,
    required this.recipients,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListView.separated(
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        itemCount: recipients.length,
        separatorBuilder: (_, __) => const Divider(height: 1),
        itemBuilder: (context, index) {
          final recipient = recipients[index];
          return ListTile(
            leading: CircleAvatar(
              backgroundColor: AppColors.primary.withOpacity(0.1),
              child: Text(
                _getInitials(recipient),
                style: TextStyle(
                  color: AppColors.primary,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            title: Text(
              recipient.firstName != null && recipient.firstName!.isNotEmpty
                  ? '${recipient.firstName} ${recipient.lastName ?? ''}'.trim()
                  : recipient.email,
              overflow: TextOverflow.ellipsis,
            ),
            subtitle: Text(
              recipient.email,
              style: TextStyle(
                color: AppColors.onSurfaceVariant,
                fontSize: 12,
              ),
              overflow: TextOverflow.ellipsis,
            ),
            trailing: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  '${recipient.totalEmailsSent}',
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 18,
                  ),
                ),
                Text(
                  'emails',
                  style: TextStyle(
                    color: AppColors.onSurfaceVariant,
                    fontSize: 11,
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  String _getInitials(RecipientStats recipient) {
    if (recipient.firstName != null && recipient.firstName!.isNotEmpty) {
      final first = recipient.firstName![0].toUpperCase();
      if (recipient.lastName != null && recipient.lastName!.isNotEmpty) {
        return '$first${recipient.lastName![0].toUpperCase()}';
      }
      return first;
    }
    return recipient.email[0].toUpperCase();
  }
}
```

### heatmap_chart.dart
```dart
import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../domain/repositories/todo_repository.dart';

class HeatmapChart extends StatefulWidget {
  const HeatmapChart({super.key});

  @override
  State<HeatmapChart> createState() => _HeatmapChartState();
}

class _HeatmapChartState extends State<HeatmapChart> {
  final _todoRepository = getIt<TodoRepository>();
  Map<DateTime, int> _activityData = {};
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    final now = DateTime.now();
    final fourWeeksAgo = now.subtract(const Duration(days: 28));

    final sentEmails = await _todoRepository.getSentEmailsInRange(
      fourWeeksAgo,
      now,
    );

    // Group by date
    final Map<DateTime, int> data = {};
    for (final email in sentEmails) {
      final date = DateTime(
        email.sentAt.year,
        email.sentAt.month,
        email.sentAt.day,
      );
      data.update(date, (count) => count + 1, ifAbsent: () => 1);
    }

    setState(() {
      _activityData = data;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const SizedBox(
        height: 100,
        child: Center(child: CircularProgressIndicator()),
      );
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Day labels
            Row(
              children: ['M', 'T', 'W', 'T', 'F', 'S', 'S']
                  .map((day) => Expanded(
                        child: Text(
                          day,
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 10,
                            color: AppColors.onSurfaceVariant,
                          ),
                        ),
                      ))
                  .toList(),
            ),
            const SizedBox(height: 4),

            // Heatmap grid
            ...List.generate(4, (weekIndex) {
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 2),
                child: Row(
                  children: List.generate(7, (dayIndex) {
                    final daysAgo = (3 - weekIndex) * 7 + (6 - dayIndex);
                    final date = DateTime.now().subtract(Duration(days: daysAgo));
                    final dateKey = DateTime(date.year, date.month, date.day);
                    final count = _activityData[dateKey] ?? 0;

                    return Expanded(
                      child: Padding(
                        padding: const EdgeInsets.all(2),
                        child: AspectRatio(
                          aspectRatio: 1,
                          child: Container(
                            decoration: BoxDecoration(
                              color: _getHeatColor(count),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: count > 0
                                ? Center(
                                    child: Text(
                                      '$count',
                                      style: TextStyle(
                                        fontSize: 10,
                                        color: count > 2
                                            ? Colors.white
                                            : AppColors.onSurface,
                                      ),
                                    ),
                                  )
                                : null,
                          ),
                        ),
                      ),
                    );
                  }),
                ),
              );
            }),

            // Legend
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildLegendItem('0', AppColors.surfaceVariant),
                _buildLegendItem('1-2', AppColors.todoNew.withOpacity(0.5)),
                _buildLegendItem('3-5', AppColors.todoMedium),
                _buildLegendItem('5+', AppColors.primary),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Color _getHeatColor(int count) {
    if (count == 0) return AppColors.surfaceVariant;
    if (count <= 2) return AppColors.todoNew.withOpacity(0.5);
    if (count <= 5) return AppColors.todoMedium;
    return AppColors.primary;
  }

  Widget _buildLegendItem(String label, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8),
      child: Row(
        children: [
          Container(
            width: 12,
            height: 12,
            decoration: BoxDecoration(
              color: color,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          const SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              fontSize: 10,
              color: AppColors.onSurfaceVariant,
            ),
          ),
        ],
      ),
    );
  }
}
```

## Acceptance Criteria
- [ ] StatCard shows icon, title, value, optional subtitle
- [ ] RecipientList shows initials avatar, name, email, count
- [ ] HeatmapChart shows 4-week activity grid
- [ ] Heatmap color intensity based on count
- [ ] Legend for heatmap
- [ ] Consistent styling

## Dependencies
- Task 051 (AppColors)
- Task 080 (Statistics Use Cases for types)

## Parallel Work
Can run parallel with: Task 080, 081

## Estimated Effort
2 hours
