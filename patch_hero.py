import re
import os

# Move HeroCarousel to components
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    home_content = f.read()

hero_carousel_match = re.search(r"(@Composable\nfun HeroCarousel[\s\S]*)", home_content)
if hero_carousel_match:
    hero_carousel_code = hero_carousel_match.group(1)
    # Remove from HomeScreen
    home_content = home_content.replace(hero_carousel_code, "")
    with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
        f.write(home_content)
    
    # Create HeroCarousel.kt
    with open("app/src/main/java/com/example/ui/components/HeroCarousel.kt", "w") as f:
        f.write("package com.example.ui.components\n\n")
        f.write("import androidx.compose.foundation.background\n")
        f.write("import androidx.compose.foundation.border\n")
        f.write("import androidx.compose.foundation.clickable\n")
        f.write("import androidx.compose.foundation.layout.*\n")
        f.write("import androidx.compose.foundation.pager.*\n")
        f.write("import androidx.compose.foundation.shape.CircleShape\n")
        f.write("import androidx.compose.foundation.shape.RoundedCornerShape\n")
        f.write("import androidx.compose.material.icons.Icons\n")
        f.write("import androidx.compose.material.icons.filled.Add\n")
        f.write("import androidx.compose.material.icons.filled.PlayArrow\n")
        f.write("import androidx.compose.material3.Icon\n")
        f.write("import androidx.compose.material3.MaterialTheme\n")
        f.write("import androidx.compose.material3.Text\n")
        f.write("import androidx.compose.runtime.Composable\n")
        f.write("import androidx.compose.runtime.LaunchedEffect\n")
        f.write("import androidx.compose.ui.Alignment\n")
        f.write("import androidx.compose.ui.Modifier\n")
        f.write("import androidx.compose.ui.draw.clip\n")
        f.write("import androidx.compose.ui.graphics.Brush\n")
        f.write("import androidx.compose.ui.graphics.Color\n")
        f.write("import androidx.compose.ui.layout.ContentScale\n")
        f.write("import androidx.compose.ui.text.font.FontWeight\n")
        f.write("import androidx.compose.ui.unit.dp\n")
        f.write("import androidx.compose.ui.unit.sp\n")
        f.write("import coil.compose.AsyncImage\n")
        f.write("import kotlinx.coroutines.delay\n")
        # I'll use duck typing: I will define an interface or just pass lists of parameters
        
        f.write("""
@Composable
fun HeroCarousel(
    items: List<HeroItem>,
    onClick: (String) -> Unit
) {
    if (items.isEmpty()) return
    val pagerState = rememberPagerState(pageCount = { items.size })

    LaunchedEffect(pagerState) {
        while (true) {
            delay(3000)
            val nextPage = (pagerState.currentPage + 1) % items.size
            pagerState.animateScrollToPage(nextPage)
        }
    }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(450.dp)
    ) {
        HorizontalPager(state = pagerState, modifier = Modifier.fillMaxSize()) { page ->
            val item = items[page]
            Box(modifier = Modifier.fillMaxSize()) {
                AsyncImage(
                    model = item.backdropUrl,
                    contentDescription = item.title,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                // Background Gradient
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Transparent, Color.Black.copy(alpha = 0.9f)),
                                startY = 100f
                            )
                        )
                )

                Column(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(16.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .background(Color.White.copy(alpha = 0.2f), RoundedCornerShape(4.dp))
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Text("NEW RELEASE", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = item.title,
                        style = MaterialTheme.typography.headlineLarge,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = "An unforgettable journey\\ninto the wild",
                        color = Color.LightGray,
                        fontSize = 12.sp,
                        lineHeight = 16.sp
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(percent = 50))
                                .background(Color(0xFFE50914))
                                .clickable { onClick(item.id) }
                                .padding(horizontal = 24.dp, vertical = 10.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text("Play", color = Color.White, fontWeight = FontWeight.SemiBold)
                            }
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(CircleShape)
                                .border(1.dp, Color.White, CircleShape)
                                .clickable { /* Add to list */ },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Add", tint = Color.White)
                        }
                    }
                }
            }
        }

        // Carousel Dots
        Row(
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp),
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            repeat(items.size) { index ->
                val isSelected = pagerState.currentPage == index
                Box(
                    modifier = Modifier
                        .size(if (isSelected) 16.dp else 4.dp, 4.dp)
                        .clip(RoundedCornerShape(2.dp))
                        .background(if (isSelected) Color(0xFFE50914) else Color.Gray)
                )
            }
        }
    }
}

data class HeroItem(val id: String, val title: String, val backdropUrl: String)
""")

