import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import type { User } from "@/contexts/AuthContext";
import { updateUserProfile, fetchCurrentUser, resolveMediaUrl } from "@/lib/api";
import Sidebar from "@/components/Sidebar";
import Menubar from "@/components/Menubar";
import {
  Camera,
  Save,
  Edit3,
  User as UserIcon,
  Phone,
  Mail,
  BookOpen,
  MapPin,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

type FormData = {
  fullName: string;
  email: string;
  phone: string;
  state: string;
  district: string;
  pincode: string;
  townVillage: string;
  currentClass: string;
};

const Profile = () => {
  const { user, setUser, hydrated } = useAuth();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [profileImage, setProfileImage] = useState<string | null>(null);
  const [profileFile, setProfileFile] = useState<File | null>(null);
  const [formErrors, setFormErrors] = useState<Partial<Record<keyof FormData, string>>>({});
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [pwdErrors, setPwdErrors] = useState<{ newPassword?: string; confirmPassword?: string }>({});
  const [pwdLoading, setPwdLoading] = useState(false);

  const [formData, setFormData] = useState<FormData>({
    fullName: "",
    email: "",
    phone: "",
    state: "",
    district: "",
    pincode: "",
    townVillage: "",
    currentClass: "",
  });

  // Auth guard + load user once
  useEffect(() => {
    if (!hydrated) return;
    const tokens = localStorage.getItem("authTokens");
    if (!tokens) {
      navigate("/login", { replace: true });
      return;
    }
    const loadUser = async () => {
      try {
        if (!user) {
          const fresh = await fetchCurrentUser();
          setUser(fresh as User);
        }
      } catch (err) {
        console.error("Fetch current user error:", err);
        setError("Failed to load your profile. Please try again.");
      } finally {
        setLoading(false);
      }
    };
    loadUser();
  }, [hydrated]);

  // Sync user → form
  useEffect(() => {
    if (!user) return;

    setFormData({
      fullName: user.full_name || "",
      email: user.email || "",
      phone: user.mobile_number || "",
      state: (user.profile?.state as string) || (user as any).state || "",
      district: (user.profile?.district as string) || (user as any).district || "",
      pincode: (user.profile?.pincode as string) || (user as any).pincode || "",
      townVillage: (user.profile?.village as string) || (user as any).village || "",
      currentClass: (user.profile?.current_class as string) || (user as any).current_class || "",
    });

    const raw = (user as any).profile_picture || (user.profile as any)?.profile_image || (user as any).profile_image || "";
    const resolved = resolveMediaUrl(raw as string);
    if (resolved) setProfileImage(resolved);
  }, [user]);

  // Handle image upload
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setProfileFile(file);
      const preview = URL.createObjectURL(file);
      setProfileImage(preview);
    }
  };

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
    if (formErrors[field]) {
      setFormErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  const validateForm = (): boolean => {
    const nextErrors: Partial<Record<keyof FormData, string>> = {};
    if (!formData.fullName || formData.fullName.trim().length < 2) {
      nextErrors.fullName = "Please enter your full name";
    }
    if (formData.email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formData.email)) {
        nextErrors.email = "Enter a valid email";
      }
    }
    if (!/^\d{10}$/.test(formData.phone)) {
      nextErrors.phone = "Phone must be 10 digits";
    }
    if (formData.pincode && !/^\d{6}$/.test(formData.pincode)) {
      nextErrors.pincode = "PIN must be 6 digits";
    }
    setFormErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const validatePasswordForm = (): boolean => {
    const nextErrors: { newPassword?: string; confirmPassword?: string } = {};
    if (!newPassword || newPassword.length < 6) {
      nextErrors.newPassword = "Password must be at least 6 characters";
    }
    if (confirmPassword !== newPassword) {
      nextErrors.confirmPassword = "Passwords do not match";
    }
    setPwdErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handlePasswordSave = async () => {
    if (!validatePasswordForm()) return;
    try {
      setPwdLoading(true);
      const fd = new FormData();
      fd.append("password", newPassword);
      const response = await updateUserProfile(fd);
      if (response.data) {
        setNewPassword("");
        setConfirmPassword("");
        setPwdErrors({});
        alert("Password updated successfully!");
      } else {
        const msg = typeof response.error === 'string' ? response.error : JSON.stringify(response.error);
        alert(msg || "Failed to update password.");
        console.error(response.error);
      }
    } catch (error) {
      console.error("Error updating password:", error);
      alert("Something went wrong.");
    } finally {
      setPwdLoading(false);
    }
  };

  const handleSave = async () => {
    if (!validateForm()) {
      setIsEditing(true);
      return;
    }
    try {
      const fd = new FormData();
      fd.append("full_name", formData.fullName);
      if (formData.email) fd.append("email", formData.email);
      fd.append("mobile_number", formData.phone);
      if (formData.state) fd.append("state", formData.state);
      if (formData.district) fd.append("district", formData.district);
      if (formData.pincode) fd.append("pincode", formData.pincode);
      if (profileFile) fd.append("profile_picture", profileFile);

      const response = await updateUserProfile(fd);

      if (response.data) {
         const fresh = await fetchCurrentUser();
         setUser(fresh as User);
        alert("Profile updated successfully!");
        setIsEditing(false);
        navigate("/study");
      } else {
        const msg = typeof response.error === 'string' ? response.error : JSON.stringify(response.error);
        alert(msg || "Failed to update profile.");
        console.error(response.error);
      }
    } catch (error) {
      console.error("Error updating profile:", error);
      alert("Something went wrong.");
    }
  };

  const classOptions = [
    "BCECE",
    "DCECE",
    "UG - Botany",
    "UG - Zoology",
    "PG - Botany",
    "PG - Zoology",
  ];

  const stateOptions = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Delhi",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
  ];

  interface InputFieldProps {
    label: string;
    field: keyof FormData;
    type?: string;
    options?: string[];
    placeholder?: string;
    icon?: React.ReactNode;
    alwaysDisabled?: boolean;
    inputMode?: React.HTMLAttributes<HTMLInputElement>["inputMode"];
    maxLength?: number;
  }

  const InputField: React.FC<InputFieldProps> = ({
    label,
    field,
    type = "text",
    options,
    placeholder,
    icon,
    alwaysDisabled,
    inputMode,
    maxLength,
  }) => {
    const value = formData[field] || "";
    const errorMsg = formErrors[field];

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const rawValue = e.target.value;
      let processedValue = rawValue;

      // Apply validation rules based on field type
      if (field === "fullName") {
        processedValue = rawValue.replace(/[^a-zA-Z\s]/g, "");
        if (processedValue.length > 150) {
          processedValue = processedValue.slice(0, 150);
        }
      } else if (field === "district" || field === "townVillage") {
        processedValue = rawValue.replace(/[^a-zA-Z0-9\s]/g, "");
        if (processedValue.length > 150) {
          processedValue = processedValue.slice(0, 150);
        }
      } else if (field === "pincode") {
        processedValue = rawValue.replace(/\D/g, "");
        if (processedValue.length > 6) {
          processedValue = processedValue.slice(0, 6);
        }
      }

      handleInputChange(field, processedValue);
    };

    return (
      <div className="space-y-2">
        <Label className="flex items-center gap-2 text-sm font-medium text-gray-700">
          {icon} {label}
        </Label>

        {options ? (
          <Select
            value={value}
            disabled={!isEditing}
            onValueChange={(val) => handleInputChange(field, val)}
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder={placeholder || `Select ${label}`} />
            </SelectTrigger>
            <SelectContent>
              {options.map((option) => (
                <SelectItem key={option} value={option}>
                  {option}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        ) : (
          <Input
            type={type}
            value={value}
            onChange={handleChange}
            placeholder={placeholder}
            disabled={!isEditing || alwaysDisabled}
            inputMode={inputMode}
            maxLength={maxLength}
            aria-label={label}
            aria-invalid={!!errorMsg}
            className="w-full"
          />
        )}
        {errorMsg && (
          <p className="text-xs text-red-600 mt-1">{errorMsg}</p>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex flex-col h-screen overflow-hidden">
          <div className="sticky top-0 z-50 w-full bg-white shadow-sm">
            <Menubar className="border-b border-gray-200" />
          </div>
          <div className="flex-1 overflow-y-auto p-6">
            <div className="max-w-6xl mx-auto">
              <Card className="mb-8">
                <CardContent className="p-8">
                  <div className="flex items-center justify-between flex-wrap gap-6">
                    <div className="flex items-center gap-6">
                      <Skeleton className="h-32 w-32 rounded-full" />
                      <div className="space-y-2">
                        <Skeleton className="h-6 w-40" />
                        <Skeleton className="h-4 w-24" />
                      </div>
                    </div>
                    <Skeleton className="h-10 w-24" />
                  </div>
                </CardContent>
              </Card>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <Card>
                  <CardHeader>
                    <CardTitle>Personal Information</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                      {Array.from({ length: 8 }).map((_, i) => (
                        <Skeleton key={i} className="h-10 w-full" />
                      ))}
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Password Update</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Skeleton className="h-6 w-48" />
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center text-red-500 font-medium">{error}</div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <div className="sticky top-0 z-50 w-full bg-white shadow-sm">
          <Menubar className="border-b border-gray-200" />
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-6xl mx-auto">
            {/* Header */}
            <Card className="mb-8">
              <CardContent className="p-8">
                <div className="flex items-center justify-between flex-wrap gap-6">
                  <div className="flex items-center gap-6">
                    {/* Image */}
                    <div className="relative">
                      <div className="w-32 h-32 rounded-full overflow-hidden border-4 border-white shadow-lg bg-gray-100">
                        {profileImage ? (
                          <img
                            src={profileImage}
                            alt="Profile"
                            className="w-full h-full object-cover"
                          />
                        ) : (
                          <div className="flex items-center justify-center w-full h-full">
                            <UserIcon className="w-16 h-16 text-gray-300" />
                          </div>
                        )}
                      </div>

                      {isEditing && (
                        <label className="absolute bottom-0 right-0 bg-blue-600 p-2 rounded-full cursor-pointer text-white shadow hover:bg-blue-700 transition">
                          <Camera className="w-4 h-4" />
                          <input
                            type="file"
                            accept="image/*"
                            className="hidden"
                            onChange={handleImageUpload}
                          />
                        </label>
                      )}
                    </div>

                    <div>
                      <h1 className="text-3xl font-bold">
                        {formData.fullName || "Your Name"}
                      </h1>
                      <p className="text-gray-600">
                        {formData.currentClass || "No Exam Selected"}
                      </p>
                      {user && (user as any).role && (
                        <p className="text-sm text-gray-500">Role: {(user as any).role}</p>
                      )}
                  </div>
                </div>

                  <div className="flex gap-3">
                    {isEditing ? (
                      <>
                        <Button onClick={handleSave} className="gap-2">
                          <Save className="w-4 h-4" /> Save
                        </Button>

                        <Button
                          onClick={() => setIsEditing(false)}
                          variant="secondary"
                        >
                          Cancel
                        </Button>
                      </>
                    ) : (
                      <Button
                        onClick={() => setIsEditing(true)}
                        className="gap-2 text-white"
                      >
                        <Edit3 className="w-4 h-4" /> Edit Profile
                      </Button>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Form */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <Card>
                <CardHeader>
                  <CardTitle>Personal Information</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <InputField
                      label="Full Name"
                      field="fullName"
                      placeholder="Enter your full name"
                      icon={<UserIcon className="w-4 h-4" />}
                    />

                    <InputField
                      label="Phone Number"
                      field="phone"
                      placeholder="Enter your phone number"
                      icon={<Phone className="w-4 h-4" />}
                    />

                    <InputField
                      label="Email Address"
                      field="email"
                      placeholder="example@email.com"
                      type="email"
                      icon={<Mail className="w-4 h-4" />}
                    />

                    <InputField
                      label="Exam"
                      field="currentClass"
                      options={classOptions}
                      placeholder="Select your exam"
                      icon={<BookOpen className="w-4 h-4" />}
                    />

                    <InputField
                      label="State"
                      field="state"
                      options={stateOptions}
                      placeholder="Select your state"
                      icon={<MapPin className="w-4 h-4" />}
                    />

                    <InputField
                      label="District"
                      field="district"
                      placeholder="Enter your district"
                      icon={<MapPin className="w-4 h-4" />}
                    />

                    <InputField
                      label="Town / Village"
                      field="townVillage"
                      placeholder="Enter your town or village"
                      icon={<MapPin className="w-4 h-4" />}
                    />

                    <InputField
                      label="PIN Code"
                      field="pincode"
                      placeholder="Enter 6-digit PIN code"
                      icon={<MapPin className="w-4 h-4" />}
                      inputMode="numeric"
                      maxLength={6}
                    />
                  </div>
                </CardContent>
              </Card>

              {/* Password box */}
              <Card>
                <CardHeader>
                  <CardTitle>Password Update</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label className="text-sm font-medium text-gray-700">New Password</Label>
                      <Input
                        type="password"
                        value={newPassword}
                        onChange={(e) => {
                          setNewPassword(e.target.value);
                          if (pwdErrors.newPassword) setPwdErrors((p) => ({ ...p, newPassword: undefined }));
                        }}
                        placeholder="Enter new password"
                        aria-label="New Password"
                        aria-invalid={!!pwdErrors.newPassword}
                        disabled={pwdLoading}
                      />
                      {pwdErrors.newPassword && (
                        <p className="text-xs text-red-600 mt-1">{pwdErrors.newPassword}</p>
                      )}
                    </div>
                    <div className="space-y-2">
                      <Label className="text-sm font-medium text-gray-700">Confirm Password</Label>
                      <Input
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => {
                          setConfirmPassword(e.target.value);
                          if (pwdErrors.confirmPassword) setPwdErrors((p) => ({ ...p, confirmPassword: undefined }));
                        }}
                        placeholder="Re-enter new password"
                        aria-label="Confirm Password"
                        aria-invalid={!!pwdErrors.confirmPassword}
                        disabled={pwdLoading}
                      />
                      {pwdErrors.confirmPassword && (
                        <p className="text-xs text-red-600 mt-1">{pwdErrors.confirmPassword}</p>
                      )}
                    </div>
                  </div>
                  <div className="mt-6">
                    <Button onClick={handlePasswordSave} className="gap-2 text-white" disabled={pwdLoading}>
                      <Save className="w-4 h-4" /> Update Password
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};  

export default Profile; 
