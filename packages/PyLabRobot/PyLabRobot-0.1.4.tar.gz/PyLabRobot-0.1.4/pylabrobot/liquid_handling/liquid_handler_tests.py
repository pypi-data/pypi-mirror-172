""" Tests for LiquidHandler """
# pylint: disable=missing-class-docstring

import io
import tempfile
import textwrap
import os
import unittest
import unittest.mock
from typing import Optional

from pylabrobot.liquid_handling.resources.abstract import Tip, Well, create_equally_spaced

from . import backends
from .liquid_handler import LiquidHandler
from .resources import (
  Coordinate,
  TIP_CAR_480_A00,
  PLT_CAR_L5AC_A00,
  Cos_96_DW_1mL,
  Cos_96_DW_500ul,
  TipRack,
  TipCarrier,
  Plate,
  PlateCarrier,
  standard_volume_tip_with_filter
)
from .resources.hamilton import STARLetDeck
from .resources.ml_star import STF_L, HTF_L
from .standard import Aspiration, Dispense


class TestLiquidHandlerLayout(unittest.TestCase):
  def setUp(self):
    star = backends.Mock()
    self.lh = LiquidHandler(star, deck=STARLetDeck())

  def test_resource_assignment(self):
    tip_car = TIP_CAR_480_A00(name="tip_carrier")
    tip_car[0] = STF_L(name="tips_01")
    tip_car[1] = STF_L(name="tips_02")
    tip_car[3] = HTF_L("tips_04")

    plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
    plt_car[0] = Cos_96_DW_1mL(name="aspiration plate")
    plt_car[2] = Cos_96_DW_500ul(name="dispense plate")

    self.lh.deck.assign_child_resource(tip_car, rails=1)
    self.lh.deck.assign_child_resource(plt_car, rails=21)

    # Test placing a carrier at a location where another carrier is located.
    with self.assertRaises(ValueError):
      dbl_plt_car_1 = PLT_CAR_L5AC_A00(name="double placed carrier 1")
      self.lh.deck.assign_child_resource(dbl_plt_car_1, rails=1)

    with self.assertRaises(ValueError):
      dbl_plt_car_2 = PLT_CAR_L5AC_A00(name="double placed carrier 2")
      self.lh.deck.assign_child_resource(dbl_plt_car_2, rails=2)

    with self.assertRaises(ValueError):
      dbl_plt_car_3 = PLT_CAR_L5AC_A00(name="double placed carrier 3")
      self.lh.deck.assign_child_resource(dbl_plt_car_3, rails=20)

    # Test carrier with same name.
    with self.assertRaises(ValueError):
      same_name_carrier = PLT_CAR_L5AC_A00(name="plate carrier")
      self.lh.deck.assign_child_resource(same_name_carrier, rails=10)
    # Should not raise when replacing.
    self.lh.deck.assign_child_resource(same_name_carrier, rails=10, replace=True)
    # Should not raise when unassinged.
    self.lh.unassign_resource("plate carrier")
    self.lh.deck.assign_child_resource(same_name_carrier, rails=10, replace=True)

    # Test unassigning unassigned resource
    self.lh.unassign_resource("plate carrier")
    with self.assertRaises(KeyError):
      self.lh.unassign_resource("plate carrier")
    with self.assertRaises(KeyError):
      self.lh.unassign_resource("this resource is completely new.")

    # Test invalid rails.
    with self.assertRaises(ValueError):
      self.lh.deck.assign_child_resource(plt_car, rails=-1)
    with self.assertRaises(ValueError):
      self.lh.deck.assign_child_resource(plt_car, rails=42)
    with self.assertRaises(ValueError):
      self.lh.deck.assign_child_resource(plt_car, rails=27)

  def test_get_resource(self):
    tip_car = TIP_CAR_480_A00(name="tip_carrier")
    tip_car[0] = STF_L(name="tips_01")
    plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
    plt_car[0] = Cos_96_DW_1mL(name="aspiration plate")
    self.lh.deck.assign_child_resource(tip_car, rails=1)
    self.lh.deck.assign_child_resource(plt_car, rails=10)

    # Get resource.
    self.assertEqual(self.lh.get_resource("tip_carrier").name, "tip_carrier")
    self.assertEqual(self.lh.get_resource("plate carrier").name, "plate carrier")

    # Get subresource.
    self.assertEqual(self.lh.get_resource("tips_01").name, "tips_01")
    self.assertEqual(self.lh.get_resource("aspiration plate").name, "aspiration plate")

    # Get unknown resource.
    self.assertIsNone(self.lh.get_resource("unknown resource"))

  def test_subcoordinates(self):
    tip_car = TIP_CAR_480_A00(name="tip_carrier")
    tip_car[0] = STF_L(name="tips_01")
    tip_car[3] = HTF_L(name="tips_04")
    plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
    plt_car[0] = Cos_96_DW_1mL(name="aspiration plate")
    plt_car[2] = Cos_96_DW_500ul(name="dispense plate")
    self.lh.deck.assign_child_resource(tip_car, rails=1)
    self.lh.deck.assign_child_resource(plt_car, rails=10)

    # Rails 10 should be left of rails 1.
    self.assertGreater(self.lh.get_resource("plate carrier").get_absolute_location().x,
                       self.lh.get_resource("tip_carrier").get_absolute_location().x)

    # Verified with Hamilton Method Editor.
    # Carriers.
    self.assertEqual(self.lh.get_resource("tip_carrier").get_absolute_location(),
                     Coordinate(100.0, 63.0, 100.0))
    self.assertEqual(self.lh.get_resource("plate carrier").get_absolute_location(),
                     Coordinate(302.5, 63.0, 100.0))

    # Subresources.
    self.assertEqual(self.lh.get_resource("tips_01").get_item("A1").get_absolute_location(),
                     Coordinate(117.900, 145.800, 164.450))
    self.assertEqual(self.lh.get_resource("tips_04").get_item("A1").get_absolute_location(),
                     Coordinate(117.900, 433.800, 131.450))

    self.assertEqual(self.lh.get_resource("dispense plate").get_item("A1").get_absolute_location(),
                     Coordinate(320.500, 338.000, 188.150))
    self.assertEqual(
      self.lh.get_resource("aspiration plate").get_item("A1") .get_absolute_location(),
      Coordinate(320.500, 146.000, 187.150))

  def test_illegal_subresource_assignment_before(self):
    # Test assigning subresource with the same name as another resource in another carrier. This
    # should raise an ValueError when the carrier is assigned to the liquid handler.
    tip_car = TIP_CAR_480_A00(name="tip_carrier")
    tip_car[0] = STF_L(name="sub")
    plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
    plt_car[0] = Cos_96_DW_1mL(name="sub")
    self.lh.deck.assign_child_resource(tip_car, rails=1)
    with self.assertRaises(ValueError):
      self.lh.deck.assign_child_resource(plt_car, rails=10)

  def test_illegal_subresource_assignment_after(self):
    # Test assigning subresource with the same name as another resource in another carrier, after
    # the carrier has been assigned. This should raise an error.
    tip_car = TIP_CAR_480_A00(name="tip_carrier")
    tip_car[0] = STF_L(name="sub")
    plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
    plt_car[0] = Cos_96_DW_1mL(name="ok")
    self.lh.deck.assign_child_resource(tip_car, rails=1)
    self.lh.deck.assign_child_resource(plt_car, rails=10)
    with self.assertRaises(ValueError):
      plt_car[1] = Cos_96_DW_500ul(name="sub")

  def build_layout(self):
    tip_car = TIP_CAR_480_A00(name="tip_carrier")
    tip_car[0] = STF_L(name="tips_01")
    tip_car[1] = STF_L(name="tips_02")
    tip_car[3] = HTF_L(name="tips_04")

    plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
    plt_car[0] = Cos_96_DW_1mL(name="aspiration plate")
    plt_car[2] = Cos_96_DW_500ul(name="dispense plate")

    self.lh.deck.assign_child_resource(tip_car, rails=1)
    self.lh.deck.assign_child_resource(plt_car, rails=21)

  @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
  def test_summary(self, out):
    with self.assertRaises(ValueError):
      self.lh.summary()

    self.build_layout()
    self.maxDiff = None # pylint: disable=invalid-name
    expected_out = textwrap.dedent("""
    Rail     Resource                   Type                Coordinates (mm)
    ===============================================================================================
    (1)  ├── tip_carrier                TipCarrier          (100.000, 063.000, 100.000)
         │   ├── tips_01                TipRack             (117.900, 145.800, 164.450)
         │   ├── tips_02                TipRack             (117.900, 241.800, 164.450)
         │   ├── <empty>
         │   ├── tips_04                TipRack             (117.900, 433.800, 131.450)
         │   ├── <empty>
         │
    (21) ├── plate carrier              PlateCarrier        (550.000, 063.000, 100.000)
         │   ├── aspiration plate       Plate               (568.000, 146.000, 187.150)
         │   ├── <empty>
         │   ├── dispense plate         Plate               (568.000, 338.000, 188.150)
         │   ├── <empty>
         │   ├── <empty>
    """[1:])
    self.lh.summary()
    self.assertEqual(out.getvalue(), expected_out)

  def test_parse_lay_file(self):
    fn = "./pylabrobot/testing/test_data/test_deck.lay"
    self.lh.load_from_lay_file(fn)

    self.assertEqual(self.lh.get_resource("TIP_CAR_480_A00_0001").get_absolute_location(), \
                     Coordinate(122.500, 63.000, 100.000))
    self.assertEqual(self.lh.get_resource("tips_01").get_item("A1").get_absolute_location(), \
                     Coordinate(140.400, 145.800, 164.450))
    self.assertEqual(self.lh.get_resource("STF_L_0001").get_item("A1").get_absolute_location(), \
                     Coordinate(140.400, 241.800, 164.450))
    self.assertEqual(self.lh.get_resource("tips_04").get_item("A1").get_absolute_location(), \
                     Coordinate(140.400, 433.800, 131.450))

    self.assertEqual(self.lh.get_resource("TIP_CAR_480_A00_0001")[0].resource.name, "tips_01")
    self.assertEqual(self.lh.get_resource("TIP_CAR_480_A00_0001")[1].resource.name, "STF_L_0001")
    self.assertIsNone(self.lh.get_resource("TIP_CAR_480_A00_0001")[2].resource)
    self.assertEqual(self.lh.get_resource("TIP_CAR_480_A00_0001")[3].resource.name, "tips_04")
    self.assertIsNone(self.lh.get_resource("TIP_CAR_480_A00_0001")[4].resource)

    self.assertEqual(self.lh.get_resource("PLT_CAR_L5AC_A00_0001").get_absolute_location(), \
                     Coordinate(302.500, 63.000, 100.000))
    self.assertEqual(self.lh.get_resource("Cos_96_DW_1mL_0001").get_item("A1") \
                    .get_absolute_location(), Coordinate(320.500, 146.000, 187.150))
    self.assertEqual(self.lh.get_resource("Cos_96_DW_500ul_0001").get_item("A1") \
                    .get_absolute_location(), Coordinate(320.500, 338.000, 188.150))
    self.assertEqual(self.lh.get_resource("Cos_96_DW_1mL_0002").get_item("A1") \
                    .get_absolute_location(), Coordinate(320.500, 434.000, 187.150))
    self.assertEqual(self.lh.get_resource("Cos_96_DW_2mL_0001").get_item("A1") \
                    .get_absolute_location(), Coordinate(320.500, 530.000, 187.150))

    self.assertEqual(self.lh.get_resource("PLT_CAR_L5AC_A00_0001")[0].resource.name,
      "Cos_96_DW_1mL_0001")
    self.assertIsNone(self.lh.get_resource("PLT_CAR_L5AC_A00_0001")[1].resource)
    self.assertEqual(self.lh.get_resource("PLT_CAR_L5AC_A00_0001")[2].resource.name,
      "Cos_96_DW_500ul_0001")
    self.assertEqual(self.lh.get_resource("PLT_CAR_L5AC_A00_0001")[3].resource.name,
      "Cos_96_DW_1mL_0002")
    self.assertEqual(self.lh.get_resource("PLT_CAR_L5AC_A00_0001")[4].resource.name,
      "Cos_96_DW_2mL_0001")

    self.assertEqual(self.lh.get_resource("PLT_CAR_L5AC_A00_0002").get_absolute_location(), \
                     Coordinate(482.500, 63.000, 100.000))
    self.assertEqual(self.lh.get_resource("Cos_96_DW_1mL_0003").get_item("A1") \
                     .get_absolute_location(), Coordinate(500.500, 146.000, 187.150))
    self.assertEqual(self.lh.get_resource("Cos_96_DW_500ul_0003").get_item("A1") \
                     .get_absolute_location(), Coordinate(500.500, 242.000, 188.150))
    self.assertEqual(self.lh.get_resource("Cos_96_PCR_0001").get_item("A1") \
                     .get_absolute_location(), Coordinate(500.500, 434.000, 186.650))

    self.assertEqual(self.lh.get_resource("PLT_CAR_L5AC_A00_0002")[0].resource.name,
      "Cos_96_DW_1mL_0003")
    self.assertEqual(self.lh.get_resource("PLT_CAR_L5AC_A00_0002")[1].resource.name,
      "Cos_96_DW_500ul_0003")
    self.assertIsNone(self.lh.get_resource("PLT_CAR_L5AC_A00_0002")[2].resource)
    self.assertEqual(self.lh.get_resource("PLT_CAR_L5AC_A00_0002")[3].resource.name,
      "Cos_96_PCR_0001")
    self.assertIsNone(self.lh.get_resource("PLT_CAR_L5AC_A00_0002")[4].resource)

  def assert_same(self, lh1, lh2):
    """ Assert two liquid handler decks are the same. """
    self.assertEqual(lh1.deck.get_all_resources(), lh2.deck.get_all_resources())

  def test_json_serialization(self):
    self.maxDiff = None

    # test with standard resource classes
    self.build_layout()
    tmp_dir = tempfile.gettempdir()
    fn = os.path.join(tmp_dir, "layout.json")
    self.lh.save(fn)

    be = backends.Mock()
    recovered = LiquidHandler(be, deck=STARLetDeck())
    recovered.load_from_json(fn)

    self.assert_same(self.lh, recovered)

    # test with custom classes
    custom_1 = LiquidHandler(be, deck=STARLetDeck()) # TODO: Deck is what should be deserialized...
    tc = TipCarrier("tc", 200, 200, 200, location=Coordinate(0, 0, 0), sites=[
      Coordinate(10, 20, 30)
    ], site_size_x=10, site_size_y=10)

    tc[0] = TipRack("tips", 10, 20, 30, tip_type=standard_volume_tip_with_filter,
      items=create_equally_spaced(Tip,
        num_items_x=1, num_items_y=1,
        dx=-1, dy=-1, dz=-1,
        item_size_x=1, item_size_y=1, tip_type=standard_volume_tip_with_filter))
    pc = PlateCarrier("pc", 100, 100, 100, location=Coordinate(0, 0, 0), sites=[
      Coordinate(10, 20, 30)
    ], site_size_x=10, site_size_y=10)
    pc[0] = Plate("plate", 10, 20, 30,
      items=create_equally_spaced(Well,
        num_items_x=1, num_items_y=1,
        dx=-1, dy=-1, dz=-1,
        item_size_x=1, item_size_y=1))

    fn = os.path.join(tmp_dir, "layout.json")
    custom_1.save(fn)
    custom_recover = LiquidHandler(be, deck=STARLetDeck())
    custom_recover.load(fn)

    self.assertEqual(custom_1.deck,
                     custom_recover.deck)

    # unsupported format
    with self.assertRaises(ValueError):
      custom_recover.load(fn + ".unsupported")

  def test_move_plate_to_site(self):
    plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
    plt_car[0] = Cos_96_DW_1mL(name="plate")
    self.lh.deck.assign_child_resource(plt_car, rails=21)

    self.lh.move_plate(plt_car[0], plt_car[2])
    self.assertIsNotNone(plt_car[2].resource)
    self.assertIsNone(plt_car[0].resource)
    self.assertEqual(plt_car[2].resource, self.lh.get_resource("plate"))
    self.assertEqual(plt_car[2].resource.get_item("A1").get_absolute_location(),
                     Coordinate(568.000, 338.000, 187.150))

  def test_move_plate_free(self):
    plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
    plt_car[0] = Cos_96_DW_1mL(name="plate")
    self.lh.deck.assign_child_resource(plt_car, rails=1)

    self.lh.move_plate(plt_car[0], Coordinate(1000, 1000, 1000))
    self.assertIsNotNone(self.lh.get_resource("plate"))
    self.assertIsNone(plt_car[0].resource)
    # TODO: will probably update this test some time, when we make the deck universal and not just
    # star.
    self.assertEqual(self.lh.get_resource("plate").get_absolute_location(),
      Coordinate(1000, 1000+63, 1000+100))


class TestLiquidHandlerCommands(unittest.TestCase):
  def setUp(self):
    self.maxDiff = None

    self.lh = LiquidHandler(backends.SaverBackend(), deck=STARLetDeck())
    self.tip_rack = STF_L(name="tip_rack")
    self.plate = Cos_96_DW_1mL(name="plate")
    self.lh.deck.assign_child_resource(self.tip_rack, location=Coordinate(0, 0, 0))
    self.lh.deck.assign_child_resource(self.plate, location=Coordinate(100, 100, 0))
    self.lh.setup()

  def get_first_command(self, command) -> Optional[dict]:
    for sent_command in self.lh.backend.commands_received:
      if sent_command["command"] == command:
        return sent_command
    return None

  def test_return_tips(self):
    tips = self.tip_rack["A1"]
    self.lh.pick_up_tips(tips)
    self.lh.return_tips()

    self.assertEqual(self.get_first_command("discard_tips"), {
      "command": "discard_tips",
      "args": (tips[0],),
      "kwargs": {}})

    with self.assertRaises(RuntimeError):
      self.lh.return_tips()

  def test_return_tips96(self):
    self.lh.pick_up_tips96(self.tip_rack)
    self.lh.return_tips96()

    self.assertEqual(self.get_first_command("discard_tips96"), {
      "command": "discard_tips96",
      "args": (self.tip_rack,),
      "kwargs": {}})

    with self.assertRaises(RuntimeError):
      self.lh.return_tips()

  def test_transfer(self):
    # Simple transfer
    self.lh.transfer(self.plate["A1"], self.plate["A2"], 10,
      aspiration_liquid_class=None, dispense_liquid_classes=None)

    self.assertEqual(self.get_first_command("aspirate"), {
      "command": "aspirate",
      "args": (Aspiration(resource=self.plate.get_item("A1"), volume=10.0),),
      "kwargs": {}})
    self.assertEqual(self.get_first_command("dispense"), {
      "command": "dispense",
      "args": (Dispense(resource=self.plate.get_item("A2"), volume=10.0),),
      "kwargs": {}})
    self.lh.backend.clear()

    # Transfer to multiple wells
    self.lh.transfer(self.plate["A1"], self.plate["A1:H1"], source_vol=80,
      aspiration_liquid_class=None, dispense_liquid_classes=None)
    self.assertEqual(self.get_first_command("aspirate"), {
      "command": "aspirate",
      "args": (Aspiration(resource=self.plate.get_item("A1"), volume=80.0),),
      "kwargs": {}})
    self.assertEqual(self.get_first_command("dispense"), {
      "command": "dispense",
      "args": tuple(Dispense(resource=well, volume=10.0) for well in self.plate["A1:H1"]),
      "kwargs": {}})
    self.lh.backend.clear()

    # Transfer with ratios
    self.lh.transfer(self.plate["A1"], self.plate["B1:C1"], source_vol=60, ratios=[2, 1],
      aspiration_liquid_class=None, dispense_liquid_classes=None)
    self.assertEqual(self.get_first_command("aspirate"), {
      "command": "aspirate",
      "args": (Aspiration(resource=self.plate.get_item("A1"), volume=60.0),),
      "kwargs": {}})
    self.assertEqual(self.get_first_command("dispense"), {
      "command": "dispense",
      "args": (Dispense(resource=self.plate.get_item("B1"), volume=40.0),
               Dispense(resource=self.plate.get_item("C1"), volume=20.0)),
      "kwargs": {}})
    self.lh.backend.clear()

    # Transfer with target_vols
    vols = [3, 1, 4, 1, 5, 9, 6, 2]
    self.lh.transfer(self.plate["A1"], self.plate["A1:H1"], target_vols=vols,
      aspiration_liquid_class=None, dispense_liquid_classes=None)
    self.assertEqual(self.get_first_command("aspirate"), {
      "command": "aspirate",
      "args": (Aspiration(resource=self.plate.get_item("A1"), volume=sum(vols)),),
      "kwargs": {}})
    self.assertEqual(self.get_first_command("dispense"), {
      "command": "dispense",
      "args":
        tuple(Dispense(resource=well, volume=vol) for well, vol in zip(self.plate["A1:H1"], vols)),
      "kwargs": {}})
    self.lh.backend.clear()

    # target_vols and source_vol specified
    with self.assertRaises(TypeError):
      self.lh.transfer(self.plate["A1"], self.plate["A1:H1"], source_vol=100, target_vols=vols)

    # target_vols and ratios specified
    with self.assertRaises(TypeError):
      self.lh.transfer(self.plate["A1"], self.plate["A1:H1"], ratios=[1]*8, target_vols=vols)

  def test_stamp(self):
    # Simple transfer
    self.lh.stamp(self.plate, self.plate, volume=10,
      aspiration_liquid_class=None, dispense_liquid_class=None)

    self.assertEqual(self.get_first_command("aspirate96"), {
      "command": "aspirate96",
      "args": (),
      "kwargs": {"plate": self.plate, "volume": 10, "flow_rate": None}})
    self.assertEqual(self.get_first_command("dispense96"), {
      "command": "dispense96",
      "args": (),
      "kwargs": {"plate": self.plate, "volume": 10, "flow_rate": None}})
    self.lh.backend.clear()


if __name__ == "__main__":
  unittest.main()
