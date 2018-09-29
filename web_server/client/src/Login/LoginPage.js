import Auth from '../Auth/Auth';
import LoginForm from './LoginForm';
import React from 'react';

class LoginPage extends React.Component {
  constructor() {
    super();

    this.state = {
      errors: {},
      user: {
        email: '',
        password: ''
      }
    };
  }

  // Post login data.
  processForm(event) {
    event.preventDefault();

    const email = this.state.user.email;
    const password = this.state.user.password;

    const url = 'http://' + window.location.hostname + ':3000/auth/login';
    const request = new Request(
      url,
      {
        method:'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: this.state.user.email,
          password: this.state.user.password
        })
      });

    // send request
    fetch(request).then(response => {
      if (response.status === 200) {
        // clear previous error data if any
        this.setState({errors: {}});

        response.json().then(json => {
          console.log(json);
          Auth.authenticateUser(json.token, email);
          // redirect to main news page
          window.location.replace('/');
        });
      } else {
        console.log('Login failed');
        response.json().then(json => {
          const errors = json.errors ? json.errors : {};
          errors.summary = json.message;
          this.setState({errors});
        });
      }
    });
  }

  changeUser(event) {
    const field = event.target.name;
    const user = this.state.user;
    user[field] = event.target.value;
  
    this.setState({user});
  }

  render() {
    return (
      <LoginForm
        onSubmit={(e) => this.processForm(e)}
        onChange={(e) => this.changeUser(e)}
        errors={this.state.errors} />
    )
  }
}

export default LoginPage;
