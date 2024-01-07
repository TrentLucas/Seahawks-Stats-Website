// QueryEntry.jsx
// 
// Contains the function to execute queries the user makes
// and contains the HTML table structure for the query result
// 
// ***ALL CODE TO BE USED TO VIEWING PURPOSES ONLY. NO REUSING CODE FROM PROJECT***
///////////////////////////////////////////////////////////////////////////////////////

import { useState } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './Table.css';



// HTML structure for the Query Result
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

// input restrictions for the query entry
Table.propTypes = {
data: PropTypes.array.isRequired,
columns: PropTypes.array.isRequired,
showTable: PropTypes.bool.isRequired,
handleToggleTable: PropTypes.func.isRequired,
tableTitle: PropTypes.string.isRequired,
tableMargin: PropTypes.number,
};


// main function to show the query entry area 
// and handle button clicks/query execution
function QueryEntry() {
    const [query, setQuery] = useState('');
    const [queryResult, setQueryResult] = useState(null);
    const [showQueryResultTable, setShowQueryResultTable] = useState(true);

    // hide and unhide table
    const handleToggleQueryResultTable = () => {
        setShowQueryResultTable(!showQueryResultTable);
    };

    // execute a query (communicate to back end with query)
    const handleExecuteQuery = () => {
    axios.post('https://seahawks-database-web.azurewebsites.net/executeQuery', { query })
        .then((res) => setQueryResult(res.data))
        .catch((err) => console.log(err));
    };

    // HTML code for the query entry area
    // displayed on webpage
    return (
        <div>
            <h2>Enter SQL Query:</h2>
            <textarea
                id="sqlQuery"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                rows={5}
                cols={80}
            ></textarea>

            <button onClick={handleExecuteQuery}>Execute Query</button>

            {queryResult && (
                <div>
                <Table
                    data={queryResult}
                    columns={queryResult && queryResult[0] ? Object.keys(queryResult[0]).map(key => ({ key, title: key })) : []}
                    showTable={showQueryResultTable}
                    handleToggleTable={handleToggleQueryResultTable}
                    tableTitle="Query Result"
                />
                </div>
            )}
        </div>

    );
}

export default QueryEntry;