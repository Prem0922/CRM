import React from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  VStack,
  Textarea,
} from '@chakra-ui/react';

interface Field {
  name: string;
  label: string;
  type: 'text' | 'number' | 'select' | 'datetime-local' | 'textarea';
  options?: string[];
}

interface EditModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  fields: Field[];
  data: Record<string, any> | null;
  onSave: (data: Record<string, any>) => void;
  onCustomerChange?: (customerId: string) => void;
}

const EditModal: React.FC<EditModalProps> = ({
  isOpen,
  onClose,
  title,
  fields,
  data,
  onSave,
  onCustomerChange,
}) => {
  const [formData, setFormData] = React.useState<Record<string, any>>(data || {});

  React.useEffect(() => {
    setFormData(data || {});
  }, [data]);

  const handleChange = (name: string, value: string | number) => {
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (name === 'customer_id' && onCustomerChange) {
      onCustomerChange(value as string);
    }
  };

  const handleSubmit = () => {
    onSave(formData);
    onClose();
  };

  const formatDateTimeForInput = (dateStr: string) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toISOString().slice(0, 16); // Format: YYYY-MM-DDThh:mm
  };

  const renderField = (field: Field) => {
    switch (field.type) {
      case 'select':
        return (
          <Select
            value={formData[field.name] || ''}
            onChange={(e) => handleChange(field.name, e.target.value)}
          >
            <option value="">Select {field.label}</option>
            {field.options?.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </Select>
        );
      case 'datetime-local':
        return (
          <Input
            type="datetime-local"
            value={formatDateTimeForInput(formData[field.name])}
            onChange={(e) => handleChange(field.name, e.target.value)}
          />
        );
      case 'textarea':
        return (
          <Textarea
            value={formData[field.name] || ''}
            onChange={(e) => handleChange(field.name, e.target.value)}
            rows={4}
            resize="vertical"
          />
        );
      default:
        return (
          <Input
            type={field.type}
            value={formData[field.name] || ''}
            onChange={(e) =>
              handleChange(
                field.name,
                field.type === 'number'
                  ? parseFloat(e.target.value)
                  : e.target.value
              )
            }
          />
        );
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="xl">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>{title}</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <VStack spacing={4}>
            {fields.map((field) => (
              <FormControl key={field.name}>
                <FormLabel>{field.label}</FormLabel>
                {renderField(field)}
              </FormControl>
            ))}
          </VStack>
        </ModalBody>

        <ModalFooter>
          <Button colorScheme="blue" mr={3} onClick={handleSubmit}>
            Save
          </Button>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default EditModal; 