// Retrieve column headers from object properties
function GetHeadings(data) {
    if (!Array.isArray(data) || data.length === 0) {
        return [];
    }
    return Object.keys(data[0]);
}

// creates a html table based on a json array filled with similar objects
export default function JsonTable({ data = [] }) {
    // Check data format
    if (!Array.isArray(data) || data.length === 0) {
        return <div>No data available, try to refresh data</div>;
    }

    const headings = GetHeadings(data);

    return (
        <table border="1" className="styled-table">
            <thead>
                <tr>
                    {headings.map((heading) => (
                        <th key={heading}>{heading}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {data.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                        {headings.map((key) => (
                            <td key={key}>{row[key]}</td>
                        ))}
                    </tr>
                ))}
            </tbody>
        </table>
    );
}