def combine_reducers(reducers: dict):
    def combined(state: dict, action):
        new_state = {}
        for key, reducer in reducers.items():
            new_state[key] = reducer(state.get(key), action)
        return new_state
    return combined