import './NewsCard.css';

import Auth from '../Auth/Auth';
import React from 'react';

class NewsCard extends React.Component{
  redirectToUrl(url, event) {
    event.preventDefault();
    // console.log("click")
    this.sendClickLog();
    window.open(url, '_blank');

  }

  sendClickLog() {
    const url = 'http://' + window.location.host +
        '/news/userId=' + Auth.getEmail() + '&newsId=' + this.props.news.digest;

    const request = new Request(encodeURI(url), {
      method: 'GET',
      headers: {
        'Authorization': 'bearer ' + Auth.getToken(),
      }
    });
    // console.log("click request from react")
    fetch(request);
    console.log('send: token: ' + Auth.getToken());
    // console.log("click request from react")
  }

  render() {
    return (
      <div className="news-container" onClick={(e) => this.redirectToUrl(this.props.news.url, e)}>
        <div className='card-panel z-depth-3'>
          <div className="row">
            <div className='col s4 fill'>
              <img src={this.props.news.urlToImage} alt='news'/>
            </div>
            <div className="col s1"/>
            <div className="col s7">
              <div className="news-intro-col">
                <div className="news-intro-panel">
                  <h4>{this.props.news.title}</h4>
                  <div className="news-description">
                    <p>{this.props.news.description}</p>
                    <div>
                      {this.props.news.source != null && <div className='chip light-blue news-chip'>{this.props.news.source}</div>}
                      {this.props.news.class != null && <div className='chip amber news-chip'>{this.props.news.class}</div>}
                      {this.props.news.reason != null && <div className='chip light-green news-chip'>{this.props.news.reason}</div>}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default NewsCard;
