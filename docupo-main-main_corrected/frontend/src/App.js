
import React from 'react';
import UploadDocument from './UploadDocument';
import ReviewRepository from './ReviewRepository';
import Notification from './Notification';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      document: null,
      repository: null,
      notification: null,
    };
  }

  handleUpload = (document) => {
    this.setState({ document });
  }

  handleReview = (repository) => {
    this.setState({ repository });
  }

  handleNotification = (notification) => {
    this.setState({ notification });
  }

  render() {
    return (
      <div className="App">
        <UploadDocument onUpload={this.handleUpload} />
        {this.state.document && <ReviewRepository document={this.state.document} onReview={this.handleReview} />}
        {this.state.repository && <Notification repository={this.state.repository} onNotification={this.handleNotification} />}
      </div>
    );
  }
}

export default App;
