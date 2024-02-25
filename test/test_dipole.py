from dipole import Dipole

def test_set_dipole_state():
    dipole = Dipole(0, 0)
    assert dipole.current_state == 0
    dipole.set_current_state(1)
    assert dipole.current_state == 1

def test_stage_flip():
    dipole = Dipole(0, 0)
    assert dipole.current_state == 0
    dipole.stage_flip()
    assert dipole.current_state == 0
    assert dipole.proposed_state == 1
    assert dipole.dirty

def test_commit_flip():
    dipole = Dipole(0, 0)
    assert dipole.current_state == 0
    dipole.stage_flip()
    dipole.commit_flip()
    assert dipole.current_state == 1
    assert dipole.proposed_state == 1
    assert not dipole.dirty