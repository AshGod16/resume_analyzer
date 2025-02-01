import React from 'react';

const AnalysisDisplay = ({ analysis }: { analysis: string }) => {
  const formatSection = (content: string) => {
    return content.split('\n').map((line, index) => {
      // Main heading (##)
      if (line.startsWith('##')) {
        return (
          <h2 key={index} className="text-2xl font-semibold text-gray-800 mb-6">
            {line.replace('##', '').trim()}
          </h2>
        );
      }
      
      // Numbered section headings (e.g., "**1. Key Skills Match:**")
      if (line.match(/^\*\*\d+\./)) {
        return (
          <h3 key={index} className="text-xl font-semibold text-gray-800 mt-8 mb-4">
            {line.replace(/\*\*/g, '').trim()}
          </h3>
        );
      }

      // Bullet points
      if (line.trim().startsWith('*')) {
        // Sub-headings within bullet points (e.g., "* **Strong Match:**")
        if (line.includes('**')) {
          const [, ...rest] = line.split('**');
          const subheading = rest[0];
          const remainingText = rest.slice(1).join('');
          return (
            <div key={index} className="flex mb-4 ml-4">
              <div className="w-4 mt-2">•</div>
              <div className="flex-1">
                <span className="font-semibold text-gray-800">{subheading} </span>
                <span className="text-gray-600 font-light">{remainingText.replace(/\*/g, '').trim()}</span>
              </div>
            </div>
          );
        }
        // Regular bullet points
        return (
          <div key={index} className="flex mb-4 ml-4">
            <div className="w-4 mt-2">•</div>
            <div className="flex-1 text-gray-600 font-light">
              {line.slice(1).trim().replace(/\*/g, '')}
            </div>
          </div>
        );
      }

      // Regular text paragraphs
      if (line.trim()) {
        return (
          <p key={index} className="text-gray-600 font-light mb-4 leading-relaxed">
            {line.replace(/\*/g, '')}
          </p>
        );
      }

      // Empty lines
      return <div key={index} className="h-2" />;
    });
  };

  return (
    <div className="space-y-2 font-sans px-2">
      {formatSection(analysis)}
    </div>
  );
};

export default AnalysisDisplay;