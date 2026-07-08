import 'package:flutter/material.dart';

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
    return Container(
      height: height,
      decoration: BoxDecoration(
        gradient: SuperkateStyle.rainbowGradient,
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
    return Container(
      width: size,
      height: size,
      decoration: const BoxDecoration(
        shape: BoxShape.circle,
        gradient: SuperkateStyle.electricGradient,
        boxShadow: SuperkateStyle.softGlow,
      ),
      child: Icon(icon, color: SuperkateStyle.ink, size: size * 0.48),
    );
  }
}
