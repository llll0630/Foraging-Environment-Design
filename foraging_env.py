import pygame
import random
from collections import deque

GRID_SIZE = 15
CELL_SIZE = 40

FLOOR = 0
WALL = 1

COLOR_WALL        = (80,  80,  80)
COLOR_FLOOR       = (220, 210, 190)
COLOR_GRID_LINE   = (200, 190, 175)
COLOR_BASE        = (70,  130, 200)
COLOR_RESOURCE    = (255, 200, 50)
COLOR_AGENT       = (80,  180, 80)
COLOR_AGENT_CARRY = (220, 80,  80)

DENSITY = {1: 0.0, 2: 0.15, 3: 0.30}

ALLOWED_ACTIONS = {"UP", "DOWN", "LEFT", "RIGHT", "PICKUP"}

MOVE = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}


class ForagingEnv:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.base_pos = (1, 1)
        self._surface = None

        self.grid = None
        self.agent_pos = None
        self.resource_pos = None
        self.carrying = False
        self.step_count = 0
        self.resources_collected = 0

    # ------------------------------------------------------------------ public

    def reset(self, difficulty=1):
        """Reset map and agent. difficulty: 1 (easy) / 2 (medium) / 3 (hard)."""
        density = DENSITY.get(difficulty, 0.0)
        self.grid = self._generate_grid(density)
        self.agent_pos = list(self.base_pos)
        self.resource_pos = self._spawn_resource()
        self.carrying = False
        self.step_count = 0
        self.resources_collected = 0
        return self._state()

    def step(self, action):
        """Execute one action. Returns state dict."""
        if action not in ALLOWED_ACTIONS:
            return self._state(action_success=False)

        self.step_count += 1
        success = True

        if action in MOVE:
            dx, dy = MOVE[action]
            ax, ay = self.agent_pos
            nx, ny = ax + dx, ay + dy
            if self.grid[ny][nx] == WALL:
                success = False
            else:
                self.agent_pos = [nx, ny]
                if self.carrying and [nx, ny] == list(self.base_pos):
                    self.carrying = False
                    self.resources_collected += 1
                    self.resource_pos = self._spawn_resource()

        elif action == "PICKUP":
            if not self.carrying and self.agent_pos == self.resource_pos:
                self.carrying = True
                self.resource_pos = None
            else:
                success = False

        return self._state(action_success=success)

    def render(self, filename="screenshot.png"):
        """Save current frame to PNG. No window is opened."""
        if self._surface is None:
            pygame.init()
            self._surface = pygame.Surface((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))

        surf = self._surface

        # tiles
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surf, COLOR_WALL if self.grid[y][x] == WALL else COLOR_FLOOR, rect)
                pygame.draw.rect(surf, COLOR_GRID_LINE, rect, 1)

        # base
        bx, by = self.base_pos
        pygame.draw.rect(surf, COLOR_BASE,
                         pygame.Rect(bx * CELL_SIZE + 4, by * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))

        # resource
        if self.resource_pos:
            rx, ry = self.resource_pos
            pygame.draw.circle(surf, COLOR_RESOURCE,
                                (rx * CELL_SIZE + CELL_SIZE // 2, ry * CELL_SIZE + CELL_SIZE // 2),
                                CELL_SIZE // 3)

        # agent
        ax, ay = self.agent_pos
        pygame.draw.circle(surf, COLOR_AGENT_CARRY if self.carrying else COLOR_AGENT,
                            (ax * CELL_SIZE + CELL_SIZE // 2, ay * CELL_SIZE + CELL_SIZE // 2),
                            CELL_SIZE // 3)

        pygame.image.save(surf, filename)
        return filename

    # ----------------------------------------------------------------- private

    def _state(self, action_success=True):
        return {
            "agent_pos":           tuple(self.agent_pos),
            "resource_pos":        tuple(self.resource_pos) if self.resource_pos else None,
            "base_pos":            self.base_pos,
            "carrying":            self.carrying,
            "action_success":      action_success,
            "step_count":          self.step_count,
            "resources_collected": self.resources_collected,
        }

    def _generate_grid(self, density):
        """Generate a connected grid. Retries until all floor cells are reachable."""
        while True:
            grid = [[FLOOR] * self.grid_size for _ in range(self.grid_size)]

            # outer walls
            for i in range(self.grid_size):
                grid[0][i] = grid[self.grid_size - 1][i] = WALL
                grid[i][0] = grid[i][self.grid_size - 1] = WALL

            # random interior walls
            if density > 0:
                for y in range(1, self.grid_size - 1):
                    for x in range(1, self.grid_size - 1):
                        if (x, y) != self.base_pos and random.random() < density:
                            grid[y][x] = WALL

            if self._all_reachable(grid):
                return grid

    def _all_reachable(self, grid):
        """BFS from base; return True if every floor cell is reachable."""
        bx, by = self.base_pos
        visited = {(bx, by)}
        queue = deque([(bx, by)])
        while queue:
            x, y = queue.popleft()
            for dx, dy in MOVE.values():
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.grid_size and 0 <= ny < self.grid_size
                        and grid[ny][nx] == FLOOR and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return all(
            (x, y) in visited
            for y in range(self.grid_size)
            for x in range(self.grid_size)
            if grid[y][x] == FLOOR
        )

    def _spawn_resource(self):
        """Pick a random floor cell that is not the base and not the agent."""
        candidates = [
            (x, y)
            for y in range(self.grid_size)
            for x in range(self.grid_size)
            if self.grid[y][x] == FLOOR
            and (x, y) != tuple(self.base_pos)
            and (x, y) != tuple(self.agent_pos)
        ]
        return list(random.choice(candidates))


# -------------------------------------------------------------------- demo run

if __name__ == "__main__":
    env = ForagingEnv()

    for diff in [1, 2, 3]:
        state = env.reset(difficulty=diff)
        path = env.render(f"difficulty_{diff}.png")
        print(f"[difficulty {diff}] screenshot -> {path}")
        print(f"  state: {state}\n")
