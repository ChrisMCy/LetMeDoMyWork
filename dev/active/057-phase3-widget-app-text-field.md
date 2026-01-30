# Task 057: Create AppTextField Widget

## Phase
3 - UI Foundation & MVP

## Description
Create reusable text input widget with validation support.

## Steps
1. Create `lib/presentation/widgets/app_text_field.dart`
2. Implement various input types
3. Add validation feedback
4. Add password visibility toggle

## Code Structure
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_dimensions.dart';

class AppTextField extends StatefulWidget {
  final String? label;
  final String? hint;
  final String? helperText;
  final String? errorText;
  final TextEditingController? controller;
  final FocusNode? focusNode;
  final TextInputType keyboardType;
  final TextInputAction textInputAction;
  final bool obscureText;
  final bool enabled;
  final bool readOnly;
  final int maxLines;
  final int? maxLength;
  final IconData? prefixIcon;
  final Widget? suffix;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;
  final VoidCallback? onTap;
  final FormFieldValidator<String>? validator;
  final List<TextInputFormatter>? inputFormatters;
  final AutovalidateMode autovalidateMode;

  const AppTextField({
    super.key,
    this.label,
    this.hint,
    this.helperText,
    this.errorText,
    this.controller,
    this.focusNode,
    this.keyboardType = TextInputType.text,
    this.textInputAction = TextInputAction.next,
    this.obscureText = false,
    this.enabled = true,
    this.readOnly = false,
    this.maxLines = 1,
    this.maxLength,
    this.prefixIcon,
    this.suffix,
    this.onChanged,
    this.onSubmitted,
    this.onTap,
    this.validator,
    this.inputFormatters,
    this.autovalidateMode = AutovalidateMode.onUserInteraction,
  });

  // Named constructors for common types
  factory AppTextField.email({
    Key? key,
    String? label,
    TextEditingController? controller,
    FocusNode? focusNode,
    ValueChanged<String>? onChanged,
    FormFieldValidator<String>? validator,
  }) {
    return AppTextField(
      key: key,
      label: label ?? 'Email',
      hint: 'example@email.com',
      controller: controller,
      focusNode: focusNode,
      keyboardType: TextInputType.emailAddress,
      prefixIcon: Icons.email_outlined,
      onChanged: onChanged,
      validator: validator ?? _emailValidator,
    );
  }

  factory AppTextField.password({
    Key? key,
    String? label,
    TextEditingController? controller,
    FocusNode? focusNode,
    ValueChanged<String>? onChanged,
    FormFieldValidator<String>? validator,
  }) {
    return AppTextField(
      key: key,
      label: label ?? 'Password',
      controller: controller,
      focusNode: focusNode,
      obscureText: true,
      prefixIcon: Icons.lock_outlined,
      onChanged: onChanged,
      validator: validator,
    );
  }

  factory AppTextField.multiline({
    Key? key,
    String? label,
    String? hint,
    TextEditingController? controller,
    int maxLines = 5,
    int? maxLength,
    ValueChanged<String>? onChanged,
  }) {
    return AppTextField(
      key: key,
      label: label,
      hint: hint,
      controller: controller,
      maxLines: maxLines,
      maxLength: maxLength,
      keyboardType: TextInputType.multiline,
      textInputAction: TextInputAction.newline,
      onChanged: onChanged,
    );
  }

  static String? _emailValidator(String? value) {
    if (value == null || value.isEmpty) {
      return 'Email is required';
    }
    final regex = RegExp(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$');
    if (!regex.hasMatch(value)) {
      return 'Enter a valid email address';
    }
    return null;
  }

  @override
  State<AppTextField> createState() => _AppTextFieldState();
}

class _AppTextFieldState extends State<AppTextField> {
  bool _obscureText = false;

  @override
  void initState() {
    super.initState();
    _obscureText = widget.obscureText;
  }

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: widget.controller,
      focusNode: widget.focusNode,
      keyboardType: widget.keyboardType,
      textInputAction: widget.textInputAction,
      obscureText: _obscureText,
      enabled: widget.enabled,
      readOnly: widget.readOnly,
      maxLines: widget.obscureText ? 1 : widget.maxLines,
      maxLength: widget.maxLength,
      onChanged: widget.onChanged,
      onFieldSubmitted: widget.onSubmitted,
      onTap: widget.onTap,
      validator: widget.validator,
      autovalidateMode: widget.autovalidateMode,
      inputFormatters: widget.inputFormatters,
      decoration: InputDecoration(
        labelText: widget.label,
        hintText: widget.hint,
        helperText: widget.helperText,
        errorText: widget.errorText,
        prefixIcon: widget.prefixIcon != null
            ? Icon(widget.prefixIcon)
            : null,
        suffixIcon: _buildSuffix(),
      ),
    );
  }

  Widget? _buildSuffix() {
    if (widget.suffix != null) return widget.suffix;

    if (widget.obscureText) {
      return IconButton(
        icon: Icon(
          _obscureText ? Icons.visibility_outlined : Icons.visibility_off_outlined,
        ),
        onPressed: () {
          setState(() {
            _obscureText = !_obscureText;
          });
        },
      );
    }

    return null;
  }
}
```

## Usage Examples
```dart
AppTextField(
  label: 'Subject',
  controller: _subjectController,
  validator: (v) => v?.isEmpty == true ? 'Required' : null,
)

AppTextField.email(
  controller: _emailController,
)

AppTextField.password(
  label: 'SMTP Password',
  controller: _passwordController,
)

AppTextField.multiline(
  label: 'Email Body',
  controller: _bodyController,
  maxLines: 5,
)
```

## Acceptance Criteria
- [ ] Standard text field with label, hint, helper, error
- [ ] Email variant with validation
- [ ] Password variant with visibility toggle
- [ ] Multiline variant
- [ ] Prefix icon support
- [ ] Custom suffix support
- [ ] Form validation integration

## Dependencies
- Task 051 (AppColors)
- Task 053 (AppDimensions)

## Parallel Work
Can run parallel with: Task 056, 058, 059

## Estimated Effort
1.5 hours
