import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  selected?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  onClick,
  selected = false,
}) => {
  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-2xl p-5 border transition-all ${
        selected
          ? 'border-amber-600 ring-2 ring-amber-500 shadow-md'
          : 'border-stone-200 shadow-xs hover:border-stone-300'
      } ${onClick ? 'cursor-pointer' : ''} ${className}`}
    >
      {children}
    </div>
  );
};

