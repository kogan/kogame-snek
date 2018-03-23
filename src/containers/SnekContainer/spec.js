import React from 'react'
import { shallow } from 'enzyme'
import GenericContainer from './index.jsx'

// TODO Sample mock test for now
describe('<GenericContainer />', () => {
  test('should render without throwing an error', () => {
    const GenericContainerComponent = () => <GenericContainer />
    const component = shallow(<GenericContainerComponent />)
    expect(component.name()).toBe('Connect(GenericContainer)')
  })
})
