import React from 'react'
import { shallow } from 'enzyme'
import GenericStatusLoading from './index.jsx'

// TODO Sample mock test for now
describe('<GenericStatusLoading />', () => {
  test('should render without throwing an error', () => {
    const GenericStatusLoadingComponent = () => <GenericStatusLoading />
    const component = shallow(<GenericStatusLoadingComponent />)
    expect(component.name()).toBe('GenericStatusLoading')
  })
})
