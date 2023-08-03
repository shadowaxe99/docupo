import React, { useState, useEffect } from 'react';

const Notification = () => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    // TODO: Replace with actual API endpoint
    fetch('/api/notifications')
      .then(response => response.json())
      .then(data => setNotifications(data));
  }, []);

  return (
    <div id="notification-area">
      {notifications.map((notification, index) => (
        <div key={index}>
          <p>{notification.message}</p>
          <p>{notification.status}</p>
        </div>
      ))}
    </div>
  );
};

export default Notification;
