import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { createStore } from 'redux'
import registerServiceWorker from './registerServiceWorker';
import { Provider } from "react-redux";
import rootReducer from './reducers';
import App from './component/App'

const Store = createStore(rootReducer)

ReactDOM.render(
    <Provider store={Store}>
        <App />
    </Provider>, 
    document.getElementById('root'));

registerServiceWorker();
