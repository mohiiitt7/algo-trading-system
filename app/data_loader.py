import pandas as pd


def load_market_data(file_path: str) -> pd.DataFrame:

    try:
        # Read CSV
        df = pd.read_csv(file_path)

        print("\n========== CSV DEBUG ==========")

        print("\n1. Original columns:")
        print(df.columns.tolist())

        print("\n2. First 5 rows:")
        print(df.head())

        print("\n3. Data shape:")
        print(df.shape)

        # Clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.replace("*", "", regex=False)
        )

        print("\n4. Cleaned columns:")
        print(df.columns.tolist())

        # Rename columns
        df = df.rename(columns={
            "Date": "datetime",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        })

        print("\n5. Columns after rename:")
        print(df.columns.tolist())

        # Required columns
        required_columns = [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        # Check missing columns
        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing columns: {missing_columns}"
            )

        # Convert datetime
        df["datetime"] = pd.to_datetime(
            df["datetime"],
            errors="coerce"
        )

        # Convert numeric columns
        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        for column in numeric_columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        print("\n6. Data types after conversion:")
        print(df.dtypes)

        print("\n7. Missing values:")
        print(df[required_columns].isna().sum())

        print("\n8. Data after conversion:")
        print(df.head())

        # Remove invalid rows
        df = df.dropna(
            subset=required_columns
        )

        print("\n9. Rows remaining after dropna:")
        print(len(df))

        if df.empty:
            raise ValueError(
                "No valid market data found in CSV."
            )

        # Sort by date
        df = df.sort_values(
            by="datetime"
        )

        # Reset index
        df = df.reset_index(drop=True)

        print("\n========== CSV SUCCESS ==========")

        return df

    except FileNotFoundError:
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    except Exception as e:
        raise RuntimeError(
            f"Failed to load market data: {e}"
        )