import React from 'react';
import clsx from 'clsx';

export interface FormFieldProps {
  /** Text label for the field */
  label: string;
  /** id of the associated input element */
  htmlFor: string;
  /** Optional description or helper text */
  description?: string;
  /** Optional error message to display */
  error?: string;
  /** Child input/select/etc. */
  children: React.ReactNode;
  /** Additional wrapper classes */
  className?: string;
}

/**
 * FormField wraps a label, field component, optional description and error message
 */
export const FormField: React.FC<FormFieldProps> = ({
  label,
  htmlFor,
  description,
  error,
  children,
  className
}) => {
  return (
    <div className={clsx('mb-4', className)}>
      <label htmlFor={htmlFor} className="block mb-2 text-sm font-medium text-neutral-800">
        {label}
      </label>
      {description && (
        <p className="mb-1 text-xs text-neutral-500">
          {description}
        </p>
      )}
      {children}
      {error && (
        <p className="mt-1 text-sm text-error-DEFAULT" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};

export default FormField;
