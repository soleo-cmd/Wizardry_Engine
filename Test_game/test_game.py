"""
Test runner using only engine parser APIs and renderer parsers.

Features:
- 8x8 Town scene (states: explore, pause) with exit tile to Dungeon
- 8x8 Dungeon scene (states: explore, pause) with exit tile back to Town
- No pygame imports in this file (renderer backends handle pygame)
- Engine systems initialized before renderer; prints on initialization

Run as module from project root:

    PYTHONPATH=. python3 -m Test_game.test_game
"""

from time import sleep
import os
import sys

# Make project importable when running as a module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.renderer.renderer_2d import Renderer2D
from engine.core.TileAndGridSystems.grid_parser import GridParser
from engine.core.TileAndGridSystems.tile import Tile, TileType, TileFlags
from engine.core.EntitySystem.entity_parser import EntityParser
from engine.core.EntitySystem.entity import EntityType, EntityFlags
from engine.core.InputSystem.input_parser import InputParser
from engine.core.InputSystem.input import Key as EKey
from engine.core.DirectionMovementSystem.direction import Direction
from engine.core.DirectionMovementSystem.movement_system import DirectionMovementSystem
from engine.core.DirectionMovementSystem.movement_parser import DirectionMovementParser
from engine.core.MessageLog.message_log_parser import MessageLogParser
from engine.core.SceneSystem.scene_parser import SceneParser
from engine.core.SceneSystem.scene import SceneType
from engine.core.ClockSystem.engineclock import EngineClock
from engine.core.CameraSystem import CameraParser, RenderMode
from engine.core.DungeonGenerationSystem import DungeonGenerationParser, DungeonConfig, GenerationAlgorithm


TILE_SIZE = 32


class TestGame:
    def __init__(self, headless: bool = True):
        # Initialize engine parsers/systems first
        self.grid_parser = GridParser()
        self.entity_parser = EntityParser()
        self.input_parser = InputParser()
        self.log = MessageLogParser()
        self.camera_parser = CameraParser()
        self.dungeon_gen_parser = DungeonGenerationParser()
        print("Engine initialized: GridParser, EntityParser, InputParser, MessageLogParser, CameraParser, DungeonGenerationParser")

        # Create town scene (static 8x8)
        town_grid = self.grid_parser.spawn_grid('town', 8, 8, default_tile=Tile(TileType.FLOOR, TileFlags.WALKABLE))
        town_grid.fill_borders(Tile(TileType.WALL, TileFlags(0)))
        town_grid.set_tile(7, 7, Tile(TileType.EXIT, TileFlags.IS_EXIT | TileFlags.WALKABLE))

        # Use SceneParser to create town scene
        self.scene_parser = SceneParser()
        town_scene = self.scene_parser.create_scene('town', SceneType.OVERWORLD)
        town_scene.data['grid'] = town_grid
        town_scene.data['exit_pos'] = (6, 6)
        town_scene.data['is_procedural'] = False
        self.scene_parser.set_current_scene('town')
        self.scenes = {'town': town_scene}

        # Spawn player entity once and place in town start
        self.player = self.entity_parser.spawn_entity('player', EntityType.PLAYER,
                                                      EntityFlags.ALIVE | EntityFlags.MOVABLE, hp=100)
        self.entity_parser.move_entity('player', 1, 1)
        self.player.data['facing'] = Direction.NORTH
        self.player.data['in_dungeon'] = False

        # Game state (must be set before _init_movement_system)
        self.current_scene = 'town'
        self.state = 'explore'  # or 'pause'

        # Initialize DirectionMovementSystem with the current grid
        self._init_movement_system()

        # Initialize cameras for different scenes
        self._init_cameras()

        # Initialize engine clock
        self.clock = EngineClock()
        self.clock.start()

        # Initialize renderer after engine
        backend = 'headless' if headless else 'pygame'
        self.renderer = Renderer2D(backend=backend)
        print(f"Renderer initialized (backend={backend})")

        # Renderer parsers
        self.drawing = self.renderer.drawing()
        self.text = self.renderer.text()

        # Build initial visuals for current scene
        self._load_scene(self.current_scene)

        # Bind inputs via parser (engine-level)
        self._bind_input()

        # HUD text
        self.hud = self.text.render_text(f"Scene: {self.current_scene} | State: {self.state}", 8, 8, font_size=14, name='hud')

        print("TestGame initialized: scenes created, player spawned, cameras ready")

    def _init_movement_system(self):
        """Initialize DirectionMovementSystem with current scene's grid."""
        scene = self.scenes[self.current_scene]
        grid = scene.data.get('grid')
        self.movement_system = DirectionMovementSystem(grid)
        self.movement_parser = DirectionMovementParser(self.movement_system)

    def _init_cameras(self):
        """Initialize cameras for different scenes."""
        # Town camera (8x8, can see whole map)
        self.camera_parser.create_camera(
            'town_camera',
            position=(4, 4, 0),
            viewport_size=(8, 8),
            zoom=1.0,
            render_mode=RenderMode.MODE_2D
        )
        
        # Dungeon camera (30x30, limited view)
        self.camera_parser.create_camera(
            'dungeon_camera',
            position=(15, 15, 0),
            viewport_size=(30, 30),
            zoom=1.0,
            render_mode=RenderMode.MODE_2D
        )
        
        self.camera_parser.set_active_camera('town_camera')

    def _load_scene(self, scene_name: str):
        scene = self.scenes[scene_name]
        grid = scene.data.get('grid')
        # Clear previous draw commands
        self.drawing.clear_all()

        # Prepare tile_cmds container on scene
        scene.data['tile_cmds'] = {}

        # Draw tiles
        for x, y, tile in grid.iterate_tiles():
            color = (50, 50, 50, 255)
            if tile.type == TileType.WALL:
                color = (30, 30, 30, 255)
            elif tile.type == TileType.EXIT:
                color = (200, 100, 0, 255)

            name = f"{scene_name}_tile_{x}_{y}"
            scene.data['tile_cmds'][(x, y)] = self.drawing.draw_rect(x * TILE_SIZE + TILE_SIZE/2,
                                                                     y * TILE_SIZE + TILE_SIZE/2,
                                                                     TILE_SIZE, TILE_SIZE,
                                                                     color=color, name=name)

        # Draw player
        px, py = self.player.position
        self.player_cmd = self.drawing.draw_rect(px * TILE_SIZE + TILE_SIZE/2,
                                                 py * TILE_SIZE + TILE_SIZE/2,
                                                 TILE_SIZE - 4, TILE_SIZE - 4,
                                                 color=(0, 0, 255, 255), name='player')

    def _bind_input(self):
        # Bind movement in 'explore' context
        from engine.core.InputSystem.input import Key

        def move_forward():
            if self.state != 'pause':
                if self.movement_parser.forward(self.player):
                    self._check_exit()
                    self._update_player_draw()

        def move_backward():
            if self.state != 'pause':
                if self.movement_parser.backward(self.player):
                    self._check_exit()
                    self._update_player_draw()

        def strafe_left():
            if self.state != 'pause':
                if self.movement_parser.left(self.player):
                    self._check_exit()
                    self._update_player_draw()

        def strafe_right():
            if self.state != 'pause':
                if self.movement_parser.right(self.player):
                    self._check_exit()
                    self._update_player_draw()

        def turn_left():
            # DirectionMovementSystem expects entity.facing but Entity uses entity.data['facing']
            self.player.data['facing'] = self.player.data['facing'].turn_left()

        def turn_right():
            # DirectionMovementSystem expects entity.facing but Entity uses entity.data['facing']
            self.player.data['facing'] = self.player.data['facing'].turn_right()

        def toggle_pause():
            self.toggle_pause()

        self.input_parser.add_context_action('explore', Key.UP, move_forward)
        self.input_parser.add_context_action('explore', Key.DOWN, move_backward)
        self.input_parser.add_context_action('explore', Key.LEFT, turn_left)
        self.input_parser.add_context_action('explore', Key.RIGHT, turn_right)
        self.input_parser.add_context_action('explore', Key.STRAFE_LEFT, strafe_left)
        self.input_parser.add_context_action('explore', Key.STRAFE_RIGHT, strafe_right)

        # Pause context has no movement bindings (keeps user in place)
        self.input_parser.set_context('explore')
        self.input_parser.bind_engine_hooks()

    def _update_player_draw(self):
        """Update player draw position based on entity position."""
        px, py = self.player.position
        self.drawing.update_position(self.player_cmd, px * TILE_SIZE + TILE_SIZE/2, py * TILE_SIZE + TILE_SIZE/2)

    def _check_exit(self):
        """Check if player is on exit tile and switch scenes."""
        scene = self.scenes[self.current_scene]
        if self.player.position == scene.data.get('exit_pos'):
            target = 'dungeon' if self.current_scene == 'town' else 'town'
            print(f"Player stepped on exit: switching to {target}")
            
            # Generate or load dungeon
            if target == 'dungeon':
                self._generate_dungeon()
            
            self.current_scene = target
            self.entity_parser.move_entity('player', 1, 1)
            self._init_movement_system()
            
            # Switch camera
            if target == 'dungeon':
                self.camera_parser.set_active_camera('dungeon_camera')
            else:
                self.camera_parser.set_active_camera('town_camera')
            
            self._load_scene(self.current_scene)
            self.text.update_text(self.hud, f"Scene: {self.current_scene} | State: {self.state}")

    def _generate_dungeon(self):
        """Generate procedural dungeon."""
        print("Generating procedural dungeon...")
        
        config = DungeonConfig(
            name='procedural_dungeon',
            width=30,
            height=30,
            algorithm=GenerationAlgorithm.RANDOM_ROOMS,
            target_room_count=12,
        )
        
        dungeon_grid, rooms = self.dungeon_gen_parser.generate_dungeon(config)
        print(f"Generated dungeon with {len(rooms)} rooms")
        
        # Create dungeon scene if it doesn't exist
        if 'dungeon' not in self.scenes:
            self.scene_parser = SceneParser()
            dungeon_scene = self.scene_parser.create_scene('dungeon', SceneType.OVERWORLD)
            self.scenes['dungeon'] = dungeon_scene
        
        # Store grid and rooms in scene data
        dungeon_scene = self.scenes['dungeon']
        dungeon_scene.data['grid'] = dungeon_grid
        dungeon_scene.data['rooms'] = rooms
        dungeon_scene.data['is_procedural'] = True
        dungeon_scene.data['exit_pos'] = rooms[0].get_center()  # Exit is at first room

    def _map_backend_events(self):
        # Poll backend for generic events (dicts) and map to engine InputSystem
        raw = []
        try:
            raw = self.renderer.backend.process_events()
        except Exception:
            raw = []

        for ev in raw:
            if not isinstance(ev, dict):
                continue
            etype = ev.get('type')
            key = ev.get('key')

            if etype == 'KEYDOWN' and key:
                if key == 'W':
                    self.input_parser.system.press_key(EKey.UP)
                elif key == 'S':
                    self.input_parser.system.press_key(EKey.DOWN)
                elif key == 'A':
                    self.input_parser.system.press_key(EKey.LEFT)
                elif key == 'D':
                    self.input_parser.system.press_key(EKey.RIGHT)
                elif key == 'Q':
                    self.input_parser.system.press_key(EKey.STRAFE_LEFT)
                elif key == 'E':
                    self.input_parser.system.press_key(EKey.STRAFE_RIGHT)
                elif key == 'P':
                    self.toggle_pause()
                elif key == 'ESCAPE':
                    raise SystemExit()

            elif etype == 'KEYUP' and key:
                if key == 'W':
                    self.input_parser.system.release_key(EKey.UP)
                elif key == 'S':
                    self.input_parser.system.release_key(EKey.DOWN)
                elif key == 'A':
                    self.input_parser.system.release_key(EKey.LEFT)
                elif key == 'D':
                    self.input_parser.system.release_key(EKey.RIGHT)
                elif key == 'Q':
                    self.input_parser.system.release_key(EKey.STRAFE_LEFT)
                elif key == 'E':
                    self.input_parser.system.release_key(EKey.STRAFE_RIGHT)
            elif etype == 'QUIT':
                raise SystemExit()

        # Snapshot input states
        self.input_parser.system.update()

    def run_frame(self):
        # Map backend -> engine input
        self._map_backend_events()

        # Use engine clock for timing
        self.clock.tick()
        dt = self.clock.get_delta()
        if not dt:
            dt = 1.0 / 60.0
        self.renderer.update(dt)

        # Update HUD text
        self.text.update_text(self.hud, f"Scene: {self.current_scene} | State: {self.state} | Player: {self.player.position} | Direction: {self.player.data["facing"]}")

        # Render
        self.renderer.clear()
        self.renderer.render()
        self.renderer.present()
        self.renderer.tick()

    def run(self, frames: int = 60, delay: float = 0.05):
        print("Starting main loop")
        for i in range(frames):
            try:
                self.run_frame()
            except SystemExit:
                print("Received quit signal, exiting")
                break
            print(f"Frame {i+1}: scene={self.current_scene} state={self.state} player={self.player.position}")
            sleep(delay)


if __name__ == '__main__':
    game = TestGame(headless=False)
    game.run(frames=999999)
