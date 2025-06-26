import React from 'react';
import clsx from 'clsx';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Child content inside the card */
  children: React.ReactNode;
  /** Additional classes for customization */
  className?: string;
}

/**
 * Card component provides a white background, subtle border, rounded corners and shadow.
 */
export const Card: React.FC<CardProps> = ({ children, className, ...props }) => {
  return (
    <div
      className={clsx(
        'bg-white border border-neutral.200 rounded-md shadow-md p-6',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
