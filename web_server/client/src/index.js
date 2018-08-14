import React from 'react';
import ReactDOM from 'react-dom';
import App from './App/App';
import registerServiceWorker from './registerServiceWorker';

import LoginPage from './Login/LoginPage';
import SignUpPage from './SignUp/SignUpPage'

// ReactDOM.render(<App />, document.getElementById('root'));
// registerServiceWorker();

// ReactDOM.render(<LoginPage />, document.getElementById('root'));
// registerServiceWorker();

ReactDOM.render(<SignUpPage />, document.getElementById('root'));
registerServiceWorker();
