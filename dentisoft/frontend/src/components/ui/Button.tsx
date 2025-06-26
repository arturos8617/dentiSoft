import React from 'react';
import clsx from 'clsx';

/**
 * Variants for the Button component.
 * - "default": filled primary button
 * - "outline": border-only button
 * - "text": text-only button
 */
export type ButtonVariant = 'default' | 'outline' | 'text';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual style variant */
  variant?: ButtonVariant;
  /** Additional custom classes */
  className?: string;
}

const variantStyles: Record<ButtonVariant, string> = {
  default: 'bg-primary.DEFAULT text-white hover:bg-primary.light',
  outline: 'border border-neutral.300 text-neutral.800 bg-white hover:bg-neutral.lighter',
  text: 'bg-transparent text-primary.DEFAULT hover:bg-primary.lighter',
};

/**
 * Reusable Button component using Tailwind CSS tokens.
 */
export const Button: React.FC<ButtonProps> = ({
  variant = 'default',
  className,
  children,
  ...props
}) => {
  return (
    <button
      className={clsx(
        'inline-flex items-center justify-center px-6 py-3 font-medium rounded-md',
        'focus:outline-none focus:ring-2 focus:ring-primary.subtle',
        'transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed',
        variantStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
