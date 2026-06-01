import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Download } from 'lucide-react';

export default function DataTable({ columns, data, isLoading, onRowClick }) {
  const [sortCol, setSortCol] = useState(null);
  const [sortDir, setSortDir] = useState('asc'); // 'asc' or 'desc'

  const handleSort = (key) => {
    if (sortCol === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortCol(key);
      setSortDir('asc');
    }
  };

  const sortedData = [...data].sort((a, b) => {
    if (!sortCol) return 0;
    const aVal = a[sortCol];
    const bVal = b[sortCol];
    if (aVal < bVal) return sortDir === 'asc' ? -1 : 1;
    if (aVal > bVal) return sortDir === 'asc' ? 1 : -1;
    return 0;
  });

  return (
    <div className="w-full bg-[#0d1424] border border-[#1a2840] rounded-xl overflow-hidden shadow-lg">
      <div className="flex justify-between items-center p-4 bg-[#111c30] border-b border-[#1a2840]">
        <h3 className="font-semibold text-white">Recent Sessions</h3>
        <button className="btn-secondary h-8 text-sm px-3 flex items-center gap-2 text-gray-300">
          <Download size={16} /> Export
        </button>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#111c30]">
              {columns.map((col, idx) => (
                <th 
                  key={idx}
                  onClick={() => col.sortable && handleSort(col.key)}
                  className={`p-4 text-xs font-semibold text-gray-400 uppercase tracking-wider ${col.sortable ? 'cursor-pointer hover:text-white' : ''}`}
                >
                  <div className="flex items-center gap-1">
                    {col.label}
                    {col.sortable && sortCol === col.key && (
                      sortDir === 'asc' ? <ChevronUp size={14} className="text-blue-500"/> : <ChevronDown size={14} className="text-blue-500"/>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              // Skeleton Loading
              [1, 2, 3].map(i => (
                <tr key={i} className="border-b border-[#1a2840]">
                  {columns.map((_, cIdx) => (
                    <td key={cIdx} className="p-4">
                      <div className="h-4 bg-[#1a2840] rounded animate-pulse w-3/4"></div>
                    </td>
                  ))}
                </tr>
              ))
            ) : sortedData.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="p-8 text-center text-gray-500">
                  No data available.
                </td>
              </tr>
            ) : (
              sortedData.map((row, rIdx) => (
                <tr 
                  key={rIdx} 
                  onClick={() => onRowClick && onRowClick(row)}
                  className="border-b border-[#1a2840] hover:bg-[#111c30] transition-colors cursor-pointer"
                >
                  {columns.map((col, cIdx) => (
                    <td key={cIdx} className="p-4 text-sm text-gray-300">
                      {col.render ? col.render(row[col.key], row) : row[col.key]}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
