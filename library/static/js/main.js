 // Initialize Firebase
var config = {
    apiKey: "AIzaSyALMtNDadKwhSVYAALyHrvsq4GX9xYP9J0",
    authDomain: "test-52bcd.firebaseapp.com",
    databaseURL: "https://test-52bcd.firebaseio.com",
    projectId: "test-52bcd",
    storageBucket: "test-52bcd.appspot.com",
    messagingSenderId: "623423132548"
    };

firebase.initializeApp(config);

const permissionDivId = 'permission_div';

const messaging = firebase.messaging();

navigator.serviceWorker.register('/static/js/firebase_serviceworker.js')
.then((registration) => {

  messaging.useServiceWorker(registration);

  messaging.onTokenRefresh(function() {
    messaging.getToken()
    .then(function(refreshedToken) {
      console.log('Token refreshed.');
    })
    .catch(function(err) {
      console.log('Unable to retrieve refreshed token ', err);
    });
  });

  messaging.onMessage(function(payload) {
    console.log("Message received. ", payload);
  });

  resetUI();
});

function resetUI() {

  messaging.getToken()
  .then(function(currentToken) {
    if (currentToken) {
      console.log(currentToken);
      sendToserver(currentToken);
      updateUIForPushEnabled();
    } else {
      console.log('No Instance ID token available. Request permission to generate one.');
      updateUIForPushPermissionRequired();
    }
  })
  .catch(function(err) {
    console.log('An error occurred while retrieving token. ', err);
  });
}

function requestPermission() {
  console.log('Requesting permission...');

  messaging.requestPermission()
  .then(function() {
    console.log('Notification permission granted.');

    resetUI();
  })
  .catch(function(err) {
    console.log('Unable to get permission to notify.', err);
  });
}

function updateUIForPushEnabled() {
  showHideDiv(permissionDivId, false);
}

function updateUIForPushPermissionRequired() {
  showHideDiv(permissionDivId, true);
}

function showHideDiv(divId, show) {
  const div = document.querySelector('#' + divId);
  if (show) {
    div.style = "display: visible";
  } else {
    div.style = "display: none";
  }
}

function sendToserver(token) {
    $.ajax({
        url : '/ajax/serverTotoken/',
        data : {
            'token' : token
        },
        dataType : 'json',
        success : function(data){
            if(data.is_taken) {
                alert("ok");
            }
        }
    })
}