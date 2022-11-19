'use strict';

function initMap() {
  const map = new google.maps.Map(document.querySelector('#map'), {
    center: {
      lat: 70,
      lng: -120,
    },
    scrollwheel: false,
    zoom: 2.5,
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
    styles: MAPSTYLES, // mapStyles is defined in mapstyles.js
    mapTypeId: google.maps.MapTypeId.TERRAIN,
  });

  // When a user clicks on a fireball, an info window about that fireball will appear.
  //
  // When they click on another fireball, we want the previous info window to
  // disappear, so that only one window is open at a time.
  //
  // To do this, we'll define a single InfoWindow instance. All markers will
  // share this instance.
  const fireballInfo = new google.maps.InfoWindow();

  // Retrieving the information with AJAX.
  //
  fetch('/api/fireballs')
    .then((response) => response.json())
    .then((fireballs) => {
      for (const fireball of fireballs) {
        // Define the content of the infoWindow
        console.log(fireball)
        const fireballInfoContent = `
        <div class="window-content">
          <div class="fireball-thumbnail">
            <img
              src="/static/images/fireball.jpeg"
              alt="fireball"
            />
          </div>
          <ul class="fireball-info">
            <li><b>Fireball date: </b>${fireball.date}</li>
            <li><b>Fireball latitude: </b>${fireball.latitude}</li>
            <li><b>Fireball longitude: </b>${fireball.longitude}</li>
            <li><b>Impact energy (kt): </b>${fireball.ImpactEnergy}</li>
            
            <form action="/save_fireball" method="POST" id="fireball_id">
            <input type='text' name="fireballs_id" value=${fireball.id} hidden>
            <button type="submit">Save</button>
            </form>

          </ul>
        </div>
      `;

        const fireballMarker = new google.maps.Marker({
          position: {
            lat: fireball.latitude,
            lng: fireball.longitude,
          },
          title: `Fireball ID: ${fireball.id}}`,
          icon: {
            url: '/static/images/fireball.svg',
            scaledSize: new google.maps.Size(50, 50),
          },
          map, // same as saying map: map
        });

        fireballMarker.addListener('click', () => {
          fireballInfo.close();
          fireballInfo.setContent(fireballInfoContent);
          fireballInfo.open(map, fireballMarker);
        });
      }
    })
    .catch(() => {
      alert(`
      We were unable to retrieve data about fireballs

  
    `);
    });

  }
