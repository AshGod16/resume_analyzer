import React from 'react';

const AnalysisDisplay = ({ analysis }: { analysis: string }) => {
  // Helper function to convert markdown-style bold to JSX
  const formatBoldText = (text: string) => {
    return text.split(/(\*\*.*?\*\*)/).map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return (
          <span key={index} className="font-bold">
            {part.slice(2, -2)}
          </span>
        );
      }
      return part;
    });
  };

  // Helper function to format bullet points
  const formatBulletPoints = (text: string) => {
    const lines = text.split('\n');
    return lines.map((line, index) => {
      if (line.trim().startsWith('*')) {
        return (
          <li key={index} className="ml-4 mb-2">
            {formatBoldText(line.slice(1).trim())}
          </li>
        );
      }
      return (
        <p key={index} className="mb-4">
          {formatBoldText(line)}
        </p>
      );
    });
  };

  // Split the analysis into sections
  const sections = analysis.split('\n\n');

  return (
    <div className="space-y-6">
      {/* Overview Section */}
      <div className="mb-6">
        {formatBulletPoints(sections[0])}
      </div>

      {/* Main Sections */}
      {sections.slice(1).map((section, index) => {
        const [title, ...content] = section.split('\n');
        if (title.includes('**')) {
          return (
            <div key={index} className="mb-6">
              <h3 className="text-lg font-semibold mb-3">
                {title.replace(/\*\*/g, '')}
              </h3>
              <div className="pl-2">
                {formatBulletPoints(content.join('\n'))}
              </div>
            </div>
          );
        }
        return null;
      })}
    </div>
  );
};

export default AnalysisDisplay;