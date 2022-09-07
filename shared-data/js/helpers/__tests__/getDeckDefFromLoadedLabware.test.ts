import ot2DeckDef from '../../../deck/definitions/3/ot2_standard.json'
import ot3DeckDef from '../../../deck/definitions/3/ot3_standard.json'
import { getDeckDefFromLoadedLabware } from '..'


describe('getDeckDefFromLoadedLabware', () => {
  it('should return an OT-2 deck when the protocol is for an OT-2', () => {
    expect(getDeckDefFromLoadedLabware('OT-2')).toBe(ot2DeckDef)
  })
  it('should return an OT-3 deck when the protocol is for an OT-3', () => {
    expect(getDeckDefFromLoadedLabware('OT-3')).toBe(ot3DeckDef)
  })
})
