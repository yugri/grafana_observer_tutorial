#!/usr/bin/env python3
"""
Load testing script for the Observer application.
Generates various types of traffic to test monitoring and alerting.
"""

import argparse
import asyncio
import random
import statistics
import time
from typing import Dict, List

import aiohttp


class LoadTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.results: List[Dict] = []

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=10)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def make_request(self, endpoint: str) -> Dict:
        """Make a single request and return timing information."""
        start_time = time.time()
        try:
            async with self.session.get(f"{self.base_url}{endpoint}") as response:
                duration = time.time() - start_time
                return {
                    "endpoint": endpoint,
                    "status": response.status,
                    "duration": duration,
                    "success": response.status < 400,
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "endpoint": endpoint,
                "status": 0,
                "duration": duration,
                "success": False,
                "error": str(e),
            }

    async def normal_load(self, duration: int = 60, rps: int = 10):
        """Generate normal load with occasional errors."""
        print(f"Generating normal load: {rps} RPS for {duration} seconds")

        start_time = time.time()
        tasks = []

        while time.time() - start_time < duration:
            # Choose endpoint based on weights
            endpoints = ["/", "/health", "/simulate", "/config"]
            weights = [0.2, 0.3, 0.4, 0.1]  # 40% simulate, 30% health, etc.

            endpoint = random.choices(endpoints, weights=weights)[0]
            task = asyncio.create_task(self.make_request(endpoint))
            tasks.append(task)

            # Wait to maintain RPS
            await asyncio.sleep(1.0 / rps)

        # Wait for all tasks to complete with timeout
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True), timeout=duration + 10
            )
            self.results.extend([r for r in results if isinstance(r, dict)])
        except asyncio.TimeoutError:
            print("Warning: Some requests timed out")

        print(
            f"Completed {len([r for r in self.results if isinstance(r, dict)])} "
            f"requests"
        )

    async def error_load(self, duration: int = 30, rps: int = 5):
        """Generate load that triggers errors."""
        print(f"Generating error load: {rps} RPS for {duration} seconds")

        start_time = time.time()
        tasks = []

        while time.time() - start_time < duration:
            # Mix normal requests with error endpoints
            if random.random() < 0.7:  # 70% error endpoints
                endpoint = "/error"
            else:
                endpoint = "/simulate"

            task = asyncio.create_task(self.make_request(endpoint))
            tasks.append(task)

            await asyncio.sleep(1.0 / rps)

        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=duration + 10,
            )
            self.results.extend([r for r in results if isinstance(r, dict)])
        except asyncio.TimeoutError:
            print("Warning: Some requests timed out")

        print(
            f"Completed {len([r for r in self.results if isinstance(r, dict)])} "
            f"error requests"
        )

    async def burst_load(self, duration: int = 10, rps: int = 50):
        """Generate burst load to test high traffic scenarios."""
        print(f"Generating burst load: {rps} RPS for {duration} seconds")

        start_time = time.time()
        tasks = []

        while time.time() - start_time < duration:
            # Create multiple concurrent requests
            for _ in range(rps // 10):  # Create batches
                endpoint = random.choice(["/", "/health", "/simulate"])
                task = asyncio.create_task(self.make_request(endpoint))
                tasks.append(task)

            await asyncio.sleep(0.1)  # Small delay between batches

        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=duration + 10,
            )
            self.results.extend([r for r in results if isinstance(r, dict)])
        except asyncio.TimeoutError:
            print("Warning: Some requests timed out")

        print(
            f"Completed {len([r for r in self.results if isinstance(r, dict)])} "
            f"burst requests"
        )

    def print_summary(self):
        """Print a summary of the load test results."""
        if not self.results:
            print("No results to summarize")
            return

        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r.get("success", False))
        error_requests = total_requests - successful_requests

        durations = [r["duration"] for r in self.results]

        print("\n" + "=" * 50)
        print("LOAD TEST SUMMARY")
        print("=" * 50)
        print(f"Total Requests: {total_requests}")
        success_rate = successful_requests / total_requests * 100
        print(f"Successful: {successful_requests} ({success_rate:.1f}%)")
        error_rate = error_requests / total_requests * 100
        print(f"Errors: {error_requests} ({error_rate:.1f}%)")
        print(f"Average Response Time: {statistics.mean(durations):.3f}s")
        print(f"Median Response Time: {statistics.median(durations):.3f}s")
        percentile_95 = sorted(durations)[int(len(durations) * 0.95)]
        print(f"95th Percentile: {percentile_95:.3f}s")
        print(f"Min Response Time: {min(durations):.3f}s")
        print(f"Max Response Time: {max(durations):.3f}s")

        # Endpoint breakdown
        endpoint_stats = {}
        for result in self.results:
            endpoint = result["endpoint"]
            if endpoint not in endpoint_stats:
                endpoint_stats[endpoint] = {"total": 0, "success": 0}
            endpoint_stats[endpoint]["total"] += 1
            if result.get("success", False):
                endpoint_stats[endpoint]["success"] += 1

        print("\nEndpoint Breakdown:")
        for endpoint, stats in endpoint_stats.items():
            success_rate = stats["success"] / stats["total"] * 100
            print(
                f"  {endpoint}: {stats['total']} requests, {success_rate:.1f}% success"
            )


async def main():
    parser = argparse.ArgumentParser(description="Load test the Observer application")
    parser.add_argument(
        "--url", default="http://localhost:8000", help="Base URL of the application"
    )
    parser.add_argument(
        "--mode",
        choices=["normal", "error", "burst", "mixed"],
        default="mixed",
        help="Load test mode",
    )
    parser.add_argument(
        "--duration", type=int, default=120, help="Total test duration in seconds"
    )

    args = parser.parse_args()

    try:
        async with LoadTester(args.url) as tester:
            if args.mode == "normal":
                await tester.normal_load(args.duration)
            elif args.mode == "error":
                await tester.error_load(args.duration)
            elif args.mode == "burst":
                await tester.burst_load(args.duration)
            elif args.mode == "mixed":
                # Run a mixed scenario
                print("Running mixed load test scenario...")
                await tester.normal_load(30, 10)  # Normal load for 30s
                await tester.error_load(20, 8)  # Error load for 20s
                await tester.burst_load(10, 30)  # Burst load for 10s
                await tester.normal_load(60, 15)  # Normal load for 60s

            tester.print_summary()
    except KeyboardInterrupt:
        print("\nLoad test interrupted by user")
    except Exception as e:
        print(f"Load test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
