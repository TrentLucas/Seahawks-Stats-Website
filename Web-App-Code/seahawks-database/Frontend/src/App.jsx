// App.jsx
// 
// Highest Level function of the Front end
// Contains objects from each section of the webpage
/////////////////////////////////////////////////////

import WebTitle from './WebTitle';
import Tables from './Tables';
import QueryEntry from './QueryEntry';
import Description from './Description';



function App() {
  return (
    <div className="app-container">
      
      <div className="webTitle">
        <WebTitle />
      </div>

      <div className="description">
        <Description />
      </div>

      <img src="https://content.sportslogos.net/logos/7/180/full/seattle_seahawks_logo_primary_19765670.png" className="image1" />
      <img src="https://1000logos.net/wp-content/uploads/2017/06/Seattle-Seahawks-Logo.png" className="image2" />

      <div className="query-section">
        <QueryEntry />
      </div>

      <div className="tables-section">
        <Tables />
      </div>
    </div>
  );
}

export default App;