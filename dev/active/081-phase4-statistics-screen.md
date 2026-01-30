# Task 081: Create Statistics Screen

## Phase
4 - Advanced Features

## Description
Implement the statistics screen showing email analytics.

## Steps
1. Create `lib/presentation/screens/statistics/statistics_screen.dart`
2. Implement stat cards
3. Implement recipient list
4. Implement weekly heatmap

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../../core/di/injection.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_dimensions.dart';
import '../../../domain/usecases/statistics/get_overall_stats_usecase.dart';
import '../../../domain/usecases/statistics/get_recipient_stats_usecase.dart';
import '../../widgets/loading_indicator.dart';
import 'widgets/stat_card.dart';
import 'widgets/recipient_list.dart';
import 'widgets/heatmap_chart.dart';

class StatisticsScreen extends StatefulWidget {
  const StatisticsScreen({super.key});

  @override
  State<StatisticsScreen> createState() => _StatisticsScreenState();
}

class _StatisticsScreenState extends State<StatisticsScreen> {
  final _getOverallStats = getIt<GetOverallStatsUseCase>();
  final _getRecipientStats = getIt<GetRecipientStatsUseCase>();

  bool _isLoading = true;
  OverallStats? _overallStats;
  List<RecipientStats>? _recipientStats;

  @override
  void initState() {
    super.initState();
    _loadStats();
  }

  Future<void> _loadStats() async {
    setState(() => _isLoading = true);

    final overall = await _getOverallStats.execute();
    final recipients = await _getRecipientStats.execute();

    setState(() {
      _overallStats = overall;
      _recipientStats = recipients;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Statistics'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadStats,
          ),
        ],
      ),
      body: _isLoading
          ? const LoadingView(message: 'Loading statistics...')
          : RefreshIndicator(
              onRefresh: _loadStats,
              child: ListView(
                padding: const EdgeInsets.all(AppDimensions.paddingScreen),
                children: [
                  // Overview Cards
                  _buildOverviewSection(),
                  const SizedBox(height: 24),

                  // This Week
                  _buildThisWeekSection(),
                  const SizedBox(height: 24),

                  // Heatmap
                  _buildHeatmapSection(),
                  const SizedBox(height: 24),

                  // Top Recipients
                  _buildRecipientsSection(),
                ],
              ),
            ),
    );
  }

  Widget _buildOverviewSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Overview',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: StatCard(
                title: 'Total TODOs',
                value: '${_overallStats!.totalTodos}',
                icon: Icons.list_alt,
                color: AppColors.primary,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: StatCard(
                title: 'Emails Sent',
                value: '${_overallStats!.totalEmailsSent}',
                icon: Icons.send,
                color: AppColors.secondary,
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: StatCard(
                title: 'Active',
                value: '${_overallStats!.activeTodos}',
                icon: Icons.play_arrow,
                color: AppColors.success,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: StatCard(
                title: 'Completed',
                value: '${_overallStats!.completedTodos}',
                icon: Icons.check_circle,
                color: AppColors.todoNew,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: StatCard(
                title: 'Paused',
                value: '${_overallStats!.pausedTodos}',
                icon: Icons.pause,
                color: AppColors.warning,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildThisWeekSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'This Week',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: StatCard(
                title: 'New TODOs',
                value: '${_overallStats!.todosThisWeek}',
                icon: Icons.add_circle,
                color: AppColors.primary,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: StatCard(
                title: 'Emails Sent',
                value: '${_overallStats!.emailsThisWeek}',
                icon: Icons.email,
                color: AppColors.secondary,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildHeatmapSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Activity (Last 4 Weeks)',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 12),
        const HeatmapChart(),
      ],
    );
  }

  Widget _buildRecipientsSection() {
    if (_recipientStats == null || _recipientStats!.isEmpty) {
      return const SizedBox.shrink();
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Top Recipients',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 12),
        RecipientList(recipients: _recipientStats!.take(5).toList()),
      ],
    );
  }
}
```

## Acceptance Criteria
- [ ] Overview cards show totals
- [ ] This week stats displayed
- [ ] Heatmap shows daily activity
- [ ] Top recipients list
- [ ] Pull to refresh
- [ ] Loading state
- [ ] Empty states where needed

## Dependencies
- Task 080 (Statistics Use Cases)
- Task 082-083 (Stat widgets)

## Parallel Work
Can run parallel with: Task 080

## Estimated Effort
2-3 hours
