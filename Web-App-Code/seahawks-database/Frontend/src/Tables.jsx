// Tables.jsx
// 
// Contains the function to display all tables onto the webpage
// and the HTML structure for all of the tables
// 
// ***ALL CODE TO BE USED TO VIEWING PURPOSES ONLY. NO REUSING CODE FROM PROJECT***
///////////////////////////////////////////////////////////////////////////////////////

import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import './Table.css';



// HTML structure for the all Tables
const Table = ({ data, columns, showTable, handleToggleTable, tableTitle, tableMargin }) => (
  <div className="table-container">
    <h2 className="table-title">
      {tableTitle}
      <button className="table-toggle-button" onClick={handleToggleTable}>
        {showTable ? 'Hide Table' : 'Show Table'}
      </button>
    </h2>

    {showTable && (
      <div className="scrollable-table-container">
        <table className="table" style={{ margin: tableMargin || 0 }}>
          <thead>
            <tr className="table labels">
              {columns.map((column, index) => (
                <th key={index}>{column.title}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((rowData, rowIndex) => (
              <tr key={rowIndex} className='table row'>
                {columns.map((column, colIndex) => (
                  <td key={colIndex}>{rowData[column.key]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )}
  </div>
);

// input restrictions for the tables
Table.propTypes = {
  data: PropTypes.array.isRequired,
  columns: PropTypes.array.isRequired,
  showTable: PropTypes.bool.isRequired,
  handleToggleTable: PropTypes.func.isRequired,
  tableTitle: PropTypes.string.isRequired,
  tableMargin: PropTypes.number,
};



// main function to fetch each table in database, 
// hold column values, and send .get(table) requests to back end
function Tables() {

  // set the useState for each table
  const [tableData, setTableData] = useState({
    seasonal: [],
    offensive: [],
    defensive: [],
    specialTeams: [],
    kicker: [],
    wideReceiver: [],
    quarterback: [],
    cornerback: [],
  });

  // set the useState for the show/hide button for each table
  const [showTable, setShowTable] = useState({
    seasonal: false,
    offensive: false,
    defensive: false,
    specialTeams: false,
    kicker: false,
    wideReceiver: false,
    quarterback: false,
    cornerback: false,
  });

  // hold all table titles
  const tableTitles = {
    seasonal: 'Seasonal_Performance Table',
    offensive: 'Offensive_Team_Performance Table',
    defensive: 'Defensive_Team_Performance Table',
    specialTeams: 'Special_Team_Performance Table',
    kicker: 'Kicker_Performance Table',
    wideReceiver: 'Wide_Receiver_Performance Table',
    quarterback: 'Quarterback_Performance Table',
    cornerback: 'Cornerback_Performance Table',
  };

  // hold all table column names
  const columns = {
    seasonal: [
      { key: 'Year', title: 'Year' },
      { key: 'Reg_season_win', title: 'Reg_season_win' },
      { key: 'Reg_season_ties', title: 'Reg_season_ties' },
      { key: 'Reg_season_losses', title: 'Reg_season_losses' },
      { key: 'Playoff_appearance', title: 'Playoff_appearance' },
    ],
    offensive: [
      { key: 'Year', title: 'Year' },
      { key: 'Points_per_game', title: 'Points_per_game' },
      { key: 'Total_yards', title: 'Total_yards' },
      { key: 'Total_touchdowns', title: 'Total_touchdowns' },
    ],
    defensive: [
      { key: 'Year', title: 'Year' },
      { key: 'Total_interceptions', title: 'Total_interceptions' },
      { key: 'Total_yards_allowed', title: 'Total_yards_allowed' },
      { key: 'Points_allowed_per_game', title: 'Points_allowed_per_game' },
    ],
    specialTeams: [
      { key: 'Year', title: 'Year' },
      { key: 'Avg_punt_return_yards', title: 'Avg_punt_return_yards' },
      { key: 'Avg_kick_return_yards', title: 'Avg_kick_return_yards' },
      { key: 'FG_percentage', title: 'FG_percentage' },
    ],
    kicker: [
      { key: 'STP_year', title: 'STP_year' },
      { key: 'Name', title: 'Name' },
      { key: 'Player_number', title: 'Player_number' },
      { key: 'FG_percentage', title: 'FG_percentage' },
      { key: 'Longest_FG_made', title: 'Longest_FG_made' },
    ],
    wideReceiver: [
      { key: 'OFF_year', title: 'OFF_year' },
      { key: 'Name', title: 'Name' },
      { key: 'Player_number', title: 'Player_number' },
      { key: 'Touchdowns', title: 'Touchdowns' },
      { key: 'Receptions', title: 'Receptions' },
      { key: 'Yards', title: 'Yards' },
    ],
    quarterback: [
      { key: 'OFF_year', title: 'OFF_year' },
      { key: 'Name', title: 'Name' },
      { key: 'Player_number', title: 'Player_number' },
      { key: 'Touchdowns', title: 'Touchdowns' },
      { key: 'Interceptions', title: 'Interceptions' },
    ],
    cornerback: [
      { key: 'DEF_year', title: 'DEF_year' },
      { key: 'Name', title: 'Name' },
      { key: 'Player_number', title: 'Player_number' },
      { key: 'Interceptions', title: 'Interceptions' },
      { key: 'Forced_fumbles', title: 'Forced_fumbles' },
      { key: 'Pass_defended', title: 'Pass_defended' },
    ]
  };

  // call fetch request to back end to get table data from endpoint
  const fetchData = (endpoint, key) => {
    fetch(`https://seahawks-database-web.azurewebsites.net/${endpoint}`)
      .then((res) => res.json())
      .then((data) => setTableData((prevData) => ({ ...prevData, [key]: data })))
      .catch((err) => console.log(err));
  };

  // hide and unhide table
  const handleToggleTable = (key) => {
    setShowTable((prevShowTable) => ({ ...prevShowTable, [key]: !prevShowTable[key] }));
  };

  // execute fetchData for each table
  useEffect(() => {
    fetchData('seasonal_performance', 'seasonal');
    fetchData('offensive_team_performance', 'offensive');
    fetchData('defensive_team_performance', 'defensive');
    fetchData('special_team_performance', 'specialTeams');
    fetchData('kicker_performance', 'kicker');
    fetchData('wide_receiver_performance', 'wideReceiver');
    fetchData('quarterback_performance', 'quarterback');
    fetchData('cornerback_performance', 'cornerback');
  }, []);

  // HTML code for the tables
  // displayed on webpage
  return (
    <div>
      {Object.keys(tableData).map((key) => (
        <Table
          key={key}
          data={tableData[key]}
          columns={columns[key]}
          showTable={showTable[key]}
          handleToggleTable={() => handleToggleTable(key)}
          tableTitle={tableTitles[key]}
          tableMargin={10}
        />
      ))}
    </div>
  );
}

export default Tables;
