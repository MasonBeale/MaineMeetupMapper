import random

class BackendAnalytics:
    # Mock data generator
    @staticmethod
    def generate_analytics_data(time_range):
        """Generate mock analytics data based on time range"""
        
        # Base data structure
        data = {
            "totalEvents": random.randint(50, 200),
            "activeUsers": random.randint(100, 500),
            "avgAttendance": random.randint(20, 100),
            "popularLocations": ["Downtown", "Campus", "Westside", "East End", "North Park"],
            "topCategories": [
                {"name": "Music & Concerts", "count": random.randint(15, 45)},
                {"name": "Workshops", "count": random.randint(10, 35)},
                {"name": "Sports", "count": random.randint(8, 25)},
                {"name": "Food & Drink", "count": random.randint(12, 30)},
                {"name": "Tech Talks", "count": random.randint(5, 20)}
            ],
            "recentActivity": [
                {
                    "text": f"New event created: {random.choice(['Tech Summit', 'Music Festival', 'Workshop'])}",
                    "time": "2 hours ago"
                },
                {
                    "text": f"{random.randint(10, 50)} users joined {random.choice(['Sports Event', 'Conference'])}",
                    "time": "5 hours ago"
                },
                {
                    "text": "Monthly report generated",
                    "time": "1 day ago"
                },
                {
                    "text": "New user signup spike detected",
                    "time": "2 days ago"
                }
            ]
        }
        
        # Adjust based on time range
        if time_range == "day":
            data["totalEvents"] = random.randint(5, 20)
            data["activeUsers"] = random.randint(50, 150)
        elif time_range == "week":
            data["totalEvents"] = random.randint(20, 50)
            data["activeUsers"] = random.randint(100, 300)
        elif time_range == "month":
            data["totalEvents"] = random.randint(50, 200)
            data["activeUsers"] = random.randint(200, 500)
        elif time_range == "year":
            data["totalEvents"] = random.randint(200, 1000)
            data["activeUsers"] = random.randint(500, 2000)
        
        return data