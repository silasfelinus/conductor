import 'package:flutter/material.dart';

class SuperkatePalette {
  const SuperkatePalette({
    required this.name,
    required this.description,
    required this.ink,
    required this.midnight,
    required this.plum,
    required this.violet,
    required this.primary,
    required this.secondary,
    required this.tertiary,
    required this.accent,
    required this.soft,
    required this.muted,
    required this.quiet,
    required this.card,
    required this.cardStrong,
    required this.cardBorder,
    required this.accentBorder,
    required this.error,
    required this.spectrum,
  });

  final String name;
  final String description;
  final Color ink;
  final Color midnight;
  final Color plum;
  final Color violet;
  final Color primary;
  final Color secondary;
  final Color tertiary;
  final Color accent;
  final Color soft;
  final Color muted;
  final Color quiet;
  final Color card;
  final Color cardStrong;
  final Color cardBorder;
  final Color accentBorder;
  final Color error;
  final List<Color> spectrum;

  LinearGradient get spectrumGradient => LinearGradient(
        colors: spectrum,
        begin: Alignment.centerLeft,
        end: Alignment.centerRight,
      );

  LinearGradient get electricGradient => LinearGradient(
        colors: [primary, tertiary, secondary],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      );

  RadialGradient get nightGradient => RadialGradient(
        center: Alignment.topLeft,
        radius: 1.25,
        colors: [midnight, plum, ink],
        stops: const [0, 0.54, 1],
      );

  LinearGradient get introGradient => LinearGradient(
        colors: [plum, midnight],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      );

  LinearGradient get totalGradient => LinearGradient(
        colors: [accentBorder, plum],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      );

  List<BoxShadow> get edgeGlow => [
        BoxShadow(
          color: secondary.withAlpha(85),
          blurRadius: 28,
          offset: const Offset(0, 14),
        ),
        BoxShadow(
          color: primary.withAlpha(68),
          blurRadius: 38,
          offset: const Offset(0, 18),
        ),
      ];

  List<BoxShadow> get softGlow => [
        BoxShadow(
          color: secondary.withAlpha(51),
          blurRadius: 22,
          offset: const Offset(0, 10),
        ),
      ];

  Color get selectedChip => primary.withAlpha(56);
  Color get orbFillPrimary => primary.withAlpha(41);
  Color get orbShadowPrimary => primary.withAlpha(87);
  Color get orbFillSecondary => secondary.withAlpha(41);
  Color get orbShadowSecondary => secondary.withAlpha(87);
}

class SuperkatePalettes {
  const SuperkatePalettes._();

  static const classic = SuperkatePalette(
    name: 'Classic',
    description: 'Original dark purple and teal salon polish.',
    ink: Color(0xFF08030D),
    midnight: Color(0xFF13071E),
    plum: Color(0xFF27123A),
    violet: Color(0xFF7C4DFF),
    primary: Color(0xFFB56CFF),
    secondary: Color(0xFF14F1D9),
    tertiary: Color(0xFF7C4DFF),
    accent: Color(0xFFEDE7FF),
    soft: Color(0xFFEDE7FF),
    muted: Color(0xFFCFC2E8),
    quiet: Color(0xFF9E8CBF),
    card: Color(0xCC171124),
    cardStrong: Color(0xEE231132),
    cardBorder: Color(0xFF5A2A73),
    accentBorder: Color(0xFF1F8A80),
    error: Color(0xFFFF8FA3),
    spectrum: [Color(0xFF8B5CF6), Color(0xFF14F1D9)],
  );

  static const rainbowConnection = SuperkatePalette(
    name: 'Rainbow Connection',
    description: 'Queer-alt rainbow hair glow with spunky salon magic.',
    ink: Color(0xFF07030D),
    midnight: Color(0xFF12071F),
    plum: Color(0xFF3B1558),
    violet: Color(0xFF8B5CF6),
    primary: Color(0xFFFF4FD8),
    secondary: Color(0xFF14F1D9),
    tertiary: Color(0xFF8B5CF6),
    accent: Color(0xFFFFD166),
    soft: Color(0xFFEDE7FF),
    muted: Color(0xFFCFC2E8),
    quiet: Color(0xFF9E8CBF),
    card: Color(0xCC171124),
    cardStrong: Color(0xEE231132),
    cardBorder: Color(0xFF5A2A73),
    accentBorder: Color(0xFF1F8A80),
    error: Color(0xFFFF8FA3),
    spectrum: [
      Color(0xFFFF4FD8),
      Color(0xFFFF6B6B),
      Color(0xFFFFD166),
      Color(0xFF84F28A),
      Color(0xFF14F1D9),
      Color(0xFF38BDF8),
      Color(0xFF8B5CF6),
    ],
  );

  static const valentine = SuperkatePalette(
    name: 'Valentine',
    description: 'Cherry pink, cream, and soft glam appointment energy.',
    ink: Color(0xFF16040D),
    midnight: Color(0xFF3A0920),
    plum: Color(0xFF5A1231),
    violet: Color(0xFFB83280),
    primary: Color(0xFFFF5C93),
    secondary: Color(0xFFFFC7D6),
    tertiary: Color(0xFFE11D48),
    accent: Color(0xFFFFF1F5),
    soft: Color(0xFFFFF1F5),
    muted: Color(0xFFFFB3C7),
    quiet: Color(0xFFD9839D),
    card: Color(0xCC2A0715),
    cardStrong: Color(0xEE430B24),
    cardBorder: Color(0xFF9F3054),
    accentBorder: Color(0xFFB83280),
    error: Color(0xFFFF8FA3),
    spectrum: [Color(0xFFFF5C93), Color(0xFFFFC7D6), Color(0xFFE11D48)],
  );

  static const goth = SuperkatePalette(
    name: 'Goth',
    description: 'Black, blood red, smoke, and steel.',
    ink: Color(0xFF030303),
    midnight: Color(0xFF0B0B0D),
    plum: Color(0xFF1A0A10),
    violet: Color(0xFF4C1D2F),
    primary: Color(0xFFB91C1C),
    secondary: Color(0xFF9CA3AF),
    tertiary: Color(0xFF6B1024),
    accent: Color(0xFFE5E7EB),
    soft: Color(0xFFF3F4F6),
    muted: Color(0xFFD1D5DB),
    quiet: Color(0xFF9CA3AF),
    card: Color(0xDD0B0B0D),
    cardStrong: Color(0xF0160A0E),
    cardBorder: Color(0xFF4B111D),
    accentBorder: Color(0xFF6B7280),
    error: Color(0xFFFF7A7A),
    spectrum: [Color(0xFF0B0B0D), Color(0xFFB91C1C), Color(0xFF9CA3AF)],
  );

  static const gothPrincess = SuperkatePalette(
    name: 'Goth Princess',
    description: 'Black velvet, royal purple, hot pink, and tiara sparkle.',
    ink: Color(0xFF05020A),
    midnight: Color(0xFF12051D),
    plum: Color(0xFF2E0F4F),
    violet: Color(0xFFA855F7),
    primary: Color(0xFFFF4FD8),
    secondary: Color(0xFFFFD6FA),
    tertiary: Color(0xFFA855F7),
    accent: Color(0xFFFFD166),
    soft: Color(0xFFFFECFE),
    muted: Color(0xFFE9B8FF),
    quiet: Color(0xFFB68AD9),
    card: Color(0xDD14071F),
    cardStrong: Color(0xF0250B3A),
    cardBorder: Color(0xFF7E22CE),
    accentBorder: Color(0xFFBE185D),
    error: Color(0xFFFF8FA3),
    spectrum: [Color(0xFF05020A), Color(0xFFA855F7), Color(0xFFFF4FD8), Color(0xFFFFD166)],
  );

  static const mutant = SuperkatePalette(
    name: 'Mutant',
    description: 'Toxic green, slime violet, and radioactive teal.',
    ink: Color(0xFF041006),
    midnight: Color(0xFF06220B),
    plum: Color(0xFF1B1230),
    violet: Color(0xFF7C3AED),
    primary: Color(0xFFA3FF12),
    secondary: Color(0xFF00FFC6),
    tertiary: Color(0xFF7C3AED),
    accent: Color(0xFFE4FF7A),
    soft: Color(0xFFF0FFE6),
    muted: Color(0xFFC4FBAA),
    quiet: Color(0xFF87C981),
    card: Color(0xDD061A0A),
    cardStrong: Color(0xEE102413),
    cardBorder: Color(0xFF4ADE80),
    accentBorder: Color(0xFF059669),
    error: Color(0xFFFF8FA3),
    spectrum: [Color(0xFFA3FF12), Color(0xFF00FFC6), Color(0xFF7C3AED)],
  );

  static const cyberCandy = SuperkatePalette(
    name: 'Cyber Candy',
    description: 'Neon pink, cyan, candy blue, and arcade glow.',
    ink: Color(0xFF030617),
    midnight: Color(0xFF06112B),
    plum: Color(0xFF1E1B4B),
    violet: Color(0xFF7C3AED),
    primary: Color(0xFFFF2BD6),
    secondary: Color(0xFF22D3EE),
    tertiary: Color(0xFF60A5FA),
    accent: Color(0xFFFEF08A),
    soft: Color(0xFFE0F2FE),
    muted: Color(0xFFBAE6FD),
    quiet: Color(0xFF7DD3FC),
    card: Color(0xDD06112B),
    cardStrong: Color(0xEE111B45),
    cardBorder: Color(0xFF2563EB),
    accentBorder: Color(0xFF0891B2),
    error: Color(0xFFFF8FA3),
    spectrum: [Color(0xFFFF2BD6), Color(0xFF22D3EE), Color(0xFF60A5FA), Color(0xFFFEF08A)],
  );

  static const mermaidChrome = SuperkatePalette(
    name: 'Mermaid Chrome',
    description: 'Teal, pearl, lavender, and iridescent chrome.',
    ink: Color(0xFF031419),
    midnight: Color(0xFF062A31),
    plum: Color(0xFF183B56),
    violet: Color(0xFFC4B5FD),
    primary: Color(0xFF7DD3FC),
    secondary: Color(0xFF5EEAD4),
    tertiary: Color(0xFFC4B5FD),
    accent: Color(0xFFF8FAFC),
    soft: Color(0xFFEFF6FF),
    muted: Color(0xFFBAE6FD),
    quiet: Color(0xFF93C5FD),
    card: Color(0xDD062A31),
    cardStrong: Color(0xEE0F3440),
    cardBorder: Color(0xFF2DD4BF),
    accentBorder: Color(0xFF0891B2),
    error: Color(0xFFFF8FA3),
    spectrum: [Color(0xFF5EEAD4), Color(0xFF7DD3FC), Color(0xFFC4B5FD), Color(0xFFF8FAFC)],
  );

  static const cosmicDisco = SuperkatePalette(
    name: 'Cosmic Disco',
    description: 'Midnight blue, magenta, gold, and starfield shimmer.',
    ink: Color(0xFF050816),
    midnight: Color(0xFF0F172A),
    plum: Color(0xFF2E1065),
    violet: Color(0xFF8B5CF6),
    primary: Color(0xFFD946EF),
    secondary: Color(0xFF38BDF8),
    tertiary: Color(0xFFFFD166),
    accent: Color(0xFFFFF7AD),
    soft: Color(0xFFF5F3FF),
    muted: Color(0xFFD8B4FE),
    quiet: Color(0xFF93C5FD),
    card: Color(0xDD0F172A),
    cardStrong: Color(0xEE1E1B4B),
    cardBorder: Color(0xFF7E22CE),
    accentBorder: Color(0xFF0EA5E9),
    error: Color(0xFFFF8FA3),
    spectrum: [Color(0xFFD946EF), Color(0xFF38BDF8), Color(0xFFFFD166), Color(0xFF8B5CF6)],
  );

  static const cottageWitch = SuperkatePalette(
    name: 'Cottage Witch',
    description: 'Moss, plum, candlelight, and herb-shop warmth.',
    ink: Color(0xFF08130B),
    midnight: Color(0xFF132015),
    plum: Color(0xFF332017),
    violet: Color(0xFF6D3D2A),
    primary: Color(0xFFFACC15),
    secondary: Color(0xFF86EFAC),
    tertiary: Color(0xFFC08457),
    accent: Color(0xFFFDE68A),
    soft: Color(0xFFF7F3D8),
    muted: Color(0xFFD9D3A5),
    quiet: Color(0xFFA3B18A),
    card: Color(0xDD132015),
    cardStrong: Color(0xEE231A13),
    cardBorder: Color(0xFF4D7C0F),
    accentBorder: Color(0xFF854D0E),
    error: Color(0xFFFFA6A6),
    spectrum: [Color(0xFF86EFAC), Color(0xFFFACC15), Color(0xFFC08457), Color(0xFF6D3D2A)],
  );

  static const sunsetSorbet = SuperkatePalette(
    name: 'Sunset Sorbet',
    description: 'Coral, orange, peach, and soft purple.',
    ink: Color(0xFF1F0A10),
    midnight: Color(0xFF3A1020),
    plum: Color(0xFF5B2347),
    violet: Color(0xFFC084FC),
    primary: Color(0xFFFF7A59),
    secondary: Color(0xFFFFD166),
    tertiary: Color(0xFFC084FC),
    accent: Color(0xFFFFE4B5),
    soft: Color(0xFFFFF1E8),
    muted: Color(0xFFFFC9A7),
    quiet: Color(0xFFD89C9C),
    card: Color(0xDD35111D),
    cardStrong: Color(0xEE4A1830),
    cardBorder: Color(0xFFFF7A59),
    accentBorder: Color(0xFFEA580C),
    error: Color(0xFFFF8FA3),
    spectrum: [Color(0xFFFF7A59), Color(0xFFFFD166), Color(0xFFC084FC)],
  );

  static const midnightBarber = SuperkatePalette(
    name: 'Midnight Barber',
    description: 'Black, barber-pole red and blue, silver, crisp professional.',
    ink: Color(0xFF020617),
    midnight: Color(0xFF0F172A),
    plum: Color(0xFF111827),
    violet: Color(0xFF2563EB),
    primary: Color(0xFFEF4444),
    secondary: Color(0xFF38BDF8),
    tertiary: Color(0xFFE5E7EB),
    accent: Color(0xFFF8FAFC),
    soft: Color(0xFFF8FAFC),
    muted: Color(0xFFCBD5E1),
    quiet: Color(0xFF94A3B8),
    card: Color(0xDD0F172A),
    cardStrong: Color(0xEE111827),
    cardBorder: Color(0xFF334155),
    accentBorder: Color(0xFF1D4ED8),
    error: Color(0xFFFF8FA3),
    spectrum: [Color(0xFFEF4444), Color(0xFFE5E7EB), Color(0xFF38BDF8), Color(0xFF020617)],
  );

  static const all = [
    classic,
    rainbowConnection,
    valentine,
    goth,
    gothPrincess,
    mutant,
    cyberCandy,
    mermaidChrome,
    cosmicDisco,
    cottageWitch,
    sunsetSorbet,
    midnightBarber,
  ];
}

class SuperkateTheme extends InheritedWidget {
  const SuperkateTheme({
    super.key,
    required this.palette,
    required super.child,
  });

  final SuperkatePalette palette;

  static SuperkatePalette of(BuildContext context) {
    return context
            .dependOnInheritedWidgetOfExactType<SuperkateTheme>()
            ?.palette ??
        SuperkatePalettes.rainbowConnection;
  }

  @override
  bool updateShouldNotify(SuperkateTheme oldWidget) => palette != oldWidget.palette;
}

class SuperkateStyle {
  static const ink = Color(0xFF07030D);
  static const midnight = Color(0xFF100719);
  static const plum = Color(0xFF251037);
  static const violet = Color(0xFF8B5CF6);
  static const hotPink = Color(0xFFFF4FD8);
  static const coral = Color(0xFFFF6B6B);
  static const sun = Color(0xFFFFD166);
  static const lime = Color(0xFF84F28A);
  static const teal = Color(0xFF14F1D9);
  static const blue = Color(0xFF38BDF8);
  static const soft = Color(0xFFEDE7FF);
  static const muted = Color(0xFFCFC2E8);
  static const quiet = Color(0xFF9E8CBF);
  static const card = Color(0xCC171124);
  static const cardStrong = Color(0xEE231132);
  static const cardBorder = Color(0xFF5A2A73);
  static const tealBorder = Color(0xFF1F8A80);

  static const rainbowColors = [
    hotPink,
    coral,
    sun,
    lime,
    teal,
    blue,
    violet,
  ];

  static const rainbowGradient = LinearGradient(
    colors: rainbowColors,
    begin: Alignment.centerLeft,
    end: Alignment.centerRight,
  );

  static const electricGradient = LinearGradient(
    colors: [hotPink, violet, teal],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const nightGradient = RadialGradient(
    center: Alignment.topLeft,
    radius: 1.25,
    colors: [Color(0xFF3B1558), Color(0xFF12071F), ink],
    stops: [0, 0.54, 1],
  );

  static const edgeGlow = [
    BoxShadow(
      color: Color(0x5538BDF8),
      blurRadius: 28,
      offset: Offset(0, 14),
    ),
    BoxShadow(
      color: Color(0x44FF4FD8),
      blurRadius: 38,
      offset: Offset(0, 18),
    ),
  ];

  static const softGlow = [
    BoxShadow(
      color: Color(0x3314F1D9),
      blurRadius: 22,
      offset: Offset(0, 10),
    ),
  ];

  static RoundedRectangleBorder cardShape({Color border = cardBorder}) {
    return RoundedRectangleBorder(
      borderRadius: const BorderRadius.all(Radius.circular(28)),
      side: BorderSide(color: border),
    );
  }
}

class RainbowRail extends StatelessWidget {
  const RainbowRail({super.key, this.height = 5, this.borderRadius = 999});

  final double height;
  final double borderRadius;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);
    return Container(
      height: height,
      decoration: BoxDecoration(
        gradient: palette.spectrumGradient,
        borderRadius: BorderRadius.all(Radius.circular(borderRadius)),
      ),
    );
  }
}

class RainbowBadge extends StatelessWidget {
  const RainbowBadge({super.key, required this.icon, this.size = 58});

  final IconData icon;
  final double size;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: palette.electricGradient,
        boxShadow: palette.softGlow,
      ),
      child: Icon(icon, color: palette.ink, size: size * 0.48),
    );
  }
}
