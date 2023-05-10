import { Box, Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import Header from "../../components/Header";

const Form = () => {
  const isNonMobile = useMediaQuery("(min-width:600px)");

  const handleFormSubmit = (values) => {
    console.log(values);
  };

  return (
    <Box m="20px">
      <Header title="NEUER USER" subtitle="Erstelle einen neuen User" />

      <Formik
        onSubmit={handleFormSubmit}
        initialValues={initialValues}
        validationSchema={checkoutSchema}
      >
        {({
          values,
          errors,
          touched,
          handleBlur,
          handleChange,
          handleSubmit,
        }) => (
          <form onSubmit={handleSubmit}>
            <Box
              display="grid"
              gap="30px"
              gridTemplateColumns="repeat(4, minmax(0, 1fr))"
              sx={{
                "& > div": { gridColumn: isNonMobile ? undefined : "span 4" },
              }}
            >
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Vorname"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.firstName}
                name="first_name"
                error={!!touched.firstName && !!errors.firstName}
                helperText={touched.firstName && errors.firstName}
                sx={{ gridColumn: "span 2" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Nachname"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.lastName}
                name="last_name"
                error={!!touched.lastName && !!errors.lastName}
                helperText={touched.lastName && errors.lastName}
                sx={{ gridColumn: "span 2" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Email"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.email}
                name="email"
                error={!!touched.email && !!errors.email}
                helperText={touched.email && errors.email}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Employment Level"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.employment_level}
                name="employment_level"
                error={!!touched.employment_level && !!errors.employment_level}
                helperText={touched.employment_level && errors.employment_level}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Firmennamen"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.company_name}
                name="company_name"
                error={!!touched.company_name && !!errors.company_name}
                helperText={touched.company_name && errors.company_name}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Departement"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.departement}
                name="departement"
                error={!!touched.departement && !!errors.departement}
                helperText={touched.departement && errors.departement}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Access Level"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.access_level}
                name="access_level"
                error={!!touched.access_level && !!errors.access_level}
                helperText={touched.access_level && errors.access_level}
                sx={{ gridColumn: "span 4" }}
              />
            </Box>
            <Box display="flex" justifyContent="end" mt="20px">
              <Button type="submit" color="secondary" variant="contained">
                Create New User
              </Button>
            </Box>
          </form>
        )}
      </Formik>
    </Box>
  );
};

const phoneRegExp =
  /^((\+[1-9]{1,4}[ -]?)|(\([0-9]{2,3}\)[ -]?)|([0-9]{2,4})[ -]?)*?[0-9]{3,4}[ -]?[0-9]{3,4}$/;

const checkoutSchema = yup.object().shape({
  firstName: yup.string().required("required"),
  lastName: yup.string().required("required"),
  email: yup.string().email("invalid email").required("required"),
  employment_level: yup
    .string()
    .matches(phoneRegExp, "Phone number is not valid")
    .required("required"),
  company_name: yup.string().required("required"),
  access_level: yup.string().required("required"),
});
const initialValues = {
  firstName: "",
  lastName: "",
  email: "",
  employment_level: "",
  company_name: "",
  access_level: "",
};

export default Form;
