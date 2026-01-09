"""
Test Game Integration Tests

Verify that all engine and renderer systems work together correctly.
"""

import unittest
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from Test_game.test_game import TestGame, GameState, EntityType


class TestGameInitialization(unittest.TestCase):
    """Test game initialization."""
    
    def test_game_starts(self):
        """Test that game initializes without errors."""
        game = TestGame(headless=True)
        self.assertIsNotNone(game)
        self.assertEqual(game.current_state, GameState.EXPLORATION)
        game.shutdown()
    
    def test_player_created(self):
        """Test that player is created."""
        game = TestGame(headless=True)
        self.assertIsNotNone(game.player)
        self.assertEqual(game.player.name, "Player")
        self.assertEqual(game.player.health, 100)
        self.assertEqual(game.player.max_health, 100)
        game.shutdown()
    
    def test_enemies_created(self):
        """Test that enemies are created."""
        game = TestGame(headless=True)
        self.assertEqual(len(game.enemies), 2)
        self.assertIn("goblin_1", game.enemies)
        self.assertIn("goblin_2", game.enemies)
        game.shutdown()
    
    def test_dungeon_created(self):
        """Test that dungeon object exists."""
        game = TestGame(headless=True)
        self.assertIn("dungeon_entrance", game.objects)
        dungeon = game.objects["dungeon_entrance"]
        self.assertEqual(dungeon.name, "Dungeon Entrance")
        game.shutdown()


class TestGameplayMechanics(unittest.TestCase):
    """Test game mechanics."""
    
    def test_player_movement(self):
        """Test player movement."""
        game = TestGame(headless=True)
        initial_x = game.player.x
        initial_y = game.player.y
        
        game._move_player(10, 0)
        self.assertEqual(game.player.x, initial_x + 10)
        self.assertEqual(game.player.y, initial_y)
        
        game._move_player(0, 10)
        self.assertEqual(game.player.x, initial_x + 10)
        self.assertEqual(game.player.y, initial_y + 10)
        
        game.shutdown()
    
    def test_boundary_checking(self):
        """Test that player can't move outside boundaries."""
        game = TestGame(headless=True)
        
        # Move to edge
        game.player.x = 0
        game._move_player(-10, 0)
        self.assertEqual(game.player.x, 0)  # Shouldn't go negative
        
        # Move to opposite edge
        game.player.x = game.renderer.config.window_width - game.player.width
        game._move_player(10, 0)
        self.assertEqual(game.player.x, game.renderer.config.window_width - game.player.width)
        
        game.shutdown()
    
    def test_collision_detection(self):
        """Test collision detection."""
        game = TestGame(headless=True)
        
        enemy = game.enemies["goblin_1"]
        
        # Place player at enemy position
        game.player.x = enemy.x
        game.player.y = enemy.y
        
        # Should detect collision
        self.assertTrue(game._is_collision(game.player, enemy))
        
        # Move player away
        game.player.x += 100
        self.assertFalse(game._is_collision(game.player, enemy))
        
        game.shutdown()
    
    def test_dungeon_entry(self):
        """Test entering dungeon."""
        game = TestGame(headless=True)
        
        # Move player to dungeon
        dungeon = game.objects["dungeon_entrance"]
        game.player.x = dungeon.x
        game.player.y = dungeon.y
        
        initial_state = game.current_state
        game._enter_dungeon()
        
        self.assertEqual(game.current_state, GameState.BATTLE)
        self.assertNotEqual(game.current_state, initial_state)
        
        game.shutdown()
    
    def test_attack_nearby_enemy(self):
        """Test attacking nearby enemy."""
        game = TestGame(headless=True)
        
        # Place player at enemy location
        enemy = game.enemies["goblin_1"]
        game.player.x = enemy.x
        game.player.y = enemy.y
        
        # Attack
        game._attack_nearby_enemy()
        
        # Should enter battle
        self.assertEqual(game.current_state, GameState.BATTLE)
        
        game.shutdown()


class TestGameSystems(unittest.TestCase):
    """Test engine systems integration."""
    
    def test_state_system_integration(self):
        """Test state system is used."""
        game = TestGame(headless=True)
        
        # Check that state system has initial state
        self.assertIsNotNone(game.state_system)
        
        game.shutdown()
    
    def test_event_system_integration(self):
        """Test event system is integrated."""
        game = TestGame(headless=True)
        
        # Event system should be available
        self.assertIsNotNone(game.event_system)
        
        game.shutdown()
    
    def test_message_log_integration(self):
        """Test message log is integrated."""
        game = TestGame(headless=True)
        
        # Message log should have messages
        self.assertIsNotNone(game.message_log)
        
        game.shutdown()
    
    def test_turn_system_integration(self):
        """Test turn system is integrated."""
        game = TestGame(headless=True)
        
        # Turn system should be available
        self.assertIsNotNone(game.turn_system)
        
        game.shutdown()


class TestRendererIntegration(unittest.TestCase):
    """Test renderer integration."""
    
    def test_renderer_created(self):
        """Test renderer is created."""
        game = TestGame(headless=True)
        
        self.assertIsNotNone(game.renderer)
        self.assertEqual(game.renderer.get_backend_type(), "headless")
        
        game.shutdown()
    
    def test_drawing_system_accessible(self):
        """Test drawing API is accessible."""
        game = TestGame(headless=True)
        
        self.assertIsNotNone(game.drawing)
        
        # Test drawing
        rect_id = game.drawing.draw_rect(10, 10, 50, 50)
        self.assertIsNotNone(rect_id)
        
        game.shutdown()
    
    def test_sprite_system_accessible(self):
        """Test sprite API is accessible."""
        game = TestGame(headless=True)
        
        self.assertIsNotNone(game.sprites)
        
        # Sprites should be loaded
        player_sprite = game.sprites.get_sprite("player_sprite")
        self.assertIsNotNone(player_sprite)
        
        game.shutdown()
    
    def test_text_system_accessible(self):
        """Test text API is accessible."""
        game = TestGame(headless=True)
        
        self.assertIsNotNone(game.text)
        
        # UI text should be created
        self.assertGreater(len(game.ui_elements), 0)
        
        game.shutdown()


class TestGameLoop(unittest.TestCase):
    """Test game loop."""
    
    def test_game_loop_runs(self):
        """Test that game loop runs."""
        game = TestGame(headless=True)
        
        # Run for a few frames
        game.run(max_frames=10)
        
        # Game should have ran
        self.assertGreater(game.time, 0)
    
    def test_game_loop_processes_input(self):
        """Test that game loop processes input."""
        game = TestGame(headless=True)
        
        initial_x = game.player.x
        
        # Simulate key press (movement)
        game._move_player(20, 0)
        
        self.assertNotEqual(game.player.x, initial_x)
        
        game.shutdown()


class TestGameBalance(unittest.TestCase):
    """Test game balance and mechanics."""
    
    def test_player_health_matters(self):
        """Test that player health is tracked."""
        game = TestGame(headless=True)
        
        self.assertGreater(game.player.health, 0)
        self.assertLessEqual(game.player.health, game.player.max_health)
        
        # Damage player
        game.player.health -= 10
        self.assertEqual(game.player.health, 90)
        
        game.shutdown()
    
    def test_enemy_health_matters(self):
        """Test that enemy health is tracked."""
        game = TestGame(headless=True)
        
        enemy = game.enemies["goblin_1"]
        self.assertGreater(enemy.health, 0)
        self.assertLessEqual(enemy.health, enemy.max_health)
        
        game.shutdown()


if __name__ == "__main__":
    unittest.main()
