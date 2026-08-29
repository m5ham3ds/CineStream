import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

target = """                    }
                }
                }
            },"""

replacement = """                    }
                }
                if ((isUpdatingData || updateFinishedShowGreen) && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(if (updateFinishedShowGreen) Color(0xFF4CAF50) else primaryColorVal)
                                .padding(vertical = 4.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = if (updateFinishedShowGreen) "تم التحقق من جميع المواقع بنجاح" else stringResource(R.string.updating_data),
                                color = Color.White,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            },"""

if target in content:
    content = content.replace(target, replacement)
    print("Replaced successfully")
else:
    print("Target not found")

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
