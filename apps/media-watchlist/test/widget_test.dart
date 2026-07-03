import 'package:flutter_test/flutter_test.dart';
import 'package:media_watchlist/main.dart';

void main() {
  testWidgets('app boots', (tester) async {
    await tester.pumpWidget(const MediaWatchlistApp());
    expect(find.text('Media Watchlist'), findsWidgets);
  });
}
