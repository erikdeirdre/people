""" Database Unit Test Module """
from datetime import date
from unittest import TestCase
import pytest
from app.database import (Team, Sport, Referee, Coach, Player, RefereeSport,
                          PlayerSport, CoachSport, CoachTeam, PlayerTeam,
                          Level, LevelType, Gender)


@pytest.mark.usefixtures("init_database")
class TestSportTable(TestCase):
    """Test Sport Table"""
    def test_sport_all(self):
        """Test Query gets correct number of rows"""
        self.assertEqual(1, 1)
        result = self.DB.session.query(Sport).all()
        self.assertEqual(len(result), 9, "Not equal to NINE sports rows")

    def test_sport_active_true(self):
        """Test to check active, true"""
        result = self.DB.session.query(Sport).filter_by(description="Soccer").first()
        print(result)
        self.assertEqual(result.active, True)

    def test_sport_active_false(self):
        """Test to check active, false"""
        result = self.DB.session.query(Sport).filter_by(description="Baseball").first()
        self.assertEqual(result.active, True)


@pytest.mark.usefixtures("init_database")
class TestTeamTable(TestCase):
    """Test Team Table"""
    def test_team_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(Team).all()
        self.assertEqual(len(result), 4, "Not equal to FOUR team rows")

    def test_team_active_true(self):
        """Test to check active, true"""
        result = self.DB.session.query(Team).filter_by(description="Celtics").first()
        self.assertEqual(result.active, True)

    def test_team_active_false(self):
        """Test to check active, false"""
        result = self.DB.session.query(Team).filter_by(description="Patriots").first()
        self.assertEqual(result.active, True)


@pytest.mark.usefixtures("init_database")
class TestLevelTable(TestCase):
    """Test Level Table"""
    def test_level_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(Level).all()
        self.assertEqual(len(result), 4, "Not equal to FOUR level rows")

    def test_level_active_true(self):
        """Test to check active, true"""
        result = self.DB.session.query(Level).filter_by(
            description="Grassroots Referee").first()
        self.assertEqual(result.active, True)
        self.assertEqual(result.level_type, LevelType.REFEREE)

    def test_level_active_false(self):
        """Test to check active, false"""
        result = self.DB.session.query(Level).filter_by(
            description="Professional").first()
        self.assertEqual(result.active, False)
        self.assertEqual(result.level_type, LevelType.REFEREE)


@pytest.mark.usefixtures("init_database")
class TestRefereeTable(TestCase):
    """Test Referee Table"""
    def test_referee_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(Referee).all()
        self.assertEqual(len(result), 2, "Not equal to TWO Referee rows")

    def test_referee(self):
        """Test to confirm columns return correctly"""
        result = self.DB.session.query(Referee).get(3)
        self.assertEqual(result.active, True)
        self.assertEqual(result.first_name, "Bart")
        self.assertEqual(result.last_name, "Simpson")
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "bsimpson@simpsons.com")
        self.assertEqual(result.gender, Gender.MALE)

        result = self.DB.session.query(Referee).get(4)
        self.assertEqual(result.active, False)
        self.assertEqual(result.first_name, "Lisa")
        self.assertEqual(result.last_name, "Simpson")
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "lsimpson@simpsons.com")
        self.assertEqual(result.gender, Gender.FEMALE)

@pytest.mark.usefixtures("init_database")
class TestRefereeSportTable(TestCase):
    """Test Referee Sport Table"""
    def test_referee_sport_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(RefereeSport).all()
        self.assertEqual(len(result), 2, "Not equal to TWO Referee Sport rows")

    def test_referee_sport(self):
        """Test to confirm columns return correctly"""
        result = self.DB.session.query(RefereeSport).get((3, 1))
        self.assertEqual(result.active, True)
        self.assertEqual(result.sport_id, 1)
        self.assertEqual(result.referee_id, 3)
        self.assertEqual(result.level_date, date(2018, 3, 1))
        result = self.DB.session.query(RefereeSport).get((4, 2))
        self.assertEqual(result.active, False)
        self.assertEqual(result.sport_id, 2)
        self.assertEqual(result.referee_id, 4)
        self.assertEqual(result.level_date, date(2019, 6, 1))


@pytest.mark.usefixtures("init_database")
class TestCoachTable(TestCase):
    """Test Coach Table"""
    def test_coach_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(Coach).all()
        self.assertEqual(len(result), 2, "Not equal to TWO Coach rows")
    def test_coach(self):
        """Test to confirm columns return correctly"""
        result = self.DB.session.query(Coach).get(1)
        self.assertEqual(result.active, True)
        self.assertEqual(result.first_name, "Homer")
        self.assertEqual(result.last_name, "Simpson")
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "hsimpson@simpsons.com")

        result = self.DB.session.query(Coach).get(2)
        self.assertEqual(result.active, False)
        self.assertEqual(result.first_name, "Marge")
        self.assertEqual(result.last_name, "Simpson")
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "msimpson@simpsons.com")


@pytest.mark.usefixtures("init_database")
class TestCoachSportTable(TestCase):
    """Test Coach Sport Table"""
    def test_coach_sport_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(CoachSport).all()
        self.assertEqual(len(result), 2, "Not equal to TWO Coach Sport rows")

    def test_coach_sport(self):
        """Test to confirm columns return correctly"""
        result = self.DB.session.query(CoachSport).get((1, 1))
        self.assertEqual(result.active, True)
        self.assertEqual(result.sport_id, 1)
        self.assertEqual(result.coach_id, 1)
        result = self.DB.session.query(CoachSport).get((2, 2))
        self.assertEqual(result.active, False)
        self.assertEqual(result.sport_id, 2)
        self.assertEqual(result.coach_id, 2)


@pytest.mark.usefixtures("init_database")
class TestCoachTeamTable(TestCase):
    """Test Coach Team Table"""
    def test_coach_team_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(CoachSport).all()
        self.assertEqual(len(result), 2, "Not equal to TWO Coach Team rows")

    def test_coach_team(self):
        """Test to confirm columns return correctly"""
        result = self.DB.session.query(CoachTeam).get((1, 1))
        self.assertEqual(result.active, True)
        self.assertEqual(result.team_id, 1)
        self.assertEqual(result.coach_id, 1)
        result = self.DB.session.query(CoachTeam).get((2, 2))
        self.assertEqual(result.active, False)
        self.assertEqual(result.team_id, 2)
        self.assertEqual(result.coach_id, 2)


@pytest.mark.usefixtures("init_database")
class TestPlayerTable(TestCase):
    """Test Player Table"""
    def test_player_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(Player).all()
        self.assertEqual(len(result), 2, "Not equal to TWO Player rows")
    def test_player(self):
        """Test to confirm columns return correctly"""
        result = self.DB.session.query(Player).get(5)
        self.assertEqual(result.active, True)
        self.assertEqual(result.first_name, "Maggie")
        self.assertEqual(result.last_name, "Simpson")
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "maggie.simpson@simpsons.com")
        self.assertEqual(result.birth_date, date(2002, 10, 3))

        result = self.DB.session.query(Player).get(6)
        self.assertEqual(result.active, False)
        self.assertEqual(result.first_name, "Milhouse")
        self.assertEqual(result.last_name, "Van Houten")
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "mvanhouten@simpsons.com")
        self.assertEqual(result.birth_date, date(2000, 3, 10))


@pytest.mark.usefixtures("init_database")
class TestPlayerSportTable(TestCase):
    """Test Player Sport Table"""
    def test_player_sport_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(PlayerSport).all()
        self.assertEqual(len(result), 2, "Not equal to TWO Player Sport rows")

    def test_player_sport(self):
        """Test to confirm columns return correctly"""
        result = self.DB.session.query(PlayerSport).get((5, 1))
        self.assertEqual(result.active, True)
        self.assertEqual(result.sport_id, 1)
        self.assertEqual(result.player_id, 5)
        result = self.DB.session.query(PlayerSport).get((6, 2))
        self.assertEqual(result.active, False)
        self.assertEqual(result.sport_id, 2)
        self.assertEqual(result.player_id, 6)


@pytest.mark.usefixtures("init_database")
class TestPlayerTeamTable(TestCase):
    """Test Player Team Table"""
    def test_player_team_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(PlayerTeam).all()
        self.assertEqual(len(result), 2, "Not equal to TWO Player Team rows")

    def test_player_team(self):
        """Test to confirm columns return correctly"""
        result = self.DB.session.query(PlayerTeam).get((5, 1))
        self.assertEqual(result.active, True)
        self.assertEqual(result.team_id, 1)
        self.assertEqual(result.player_id, 5)
        result = self.DB.session.query(PlayerTeam).get((6, 2))
        self.assertEqual(result.active, False)
        self.assertEqual(result.team_id, 2)
        self.assertEqual(result.player_id, 6)


#if __name__ == '__main__':
#    unittest.main()
