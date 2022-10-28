import React, { useEffect } from 'react'
import Chart from "react-apexcharts";

const ApexChart = ({ data }) => {

	return (
		<div>
			<Chart
				type="area"
				height={800}
				width={1200}
				series={[
					{
						name: "BTC",
						data: data
					}
				]}

				options={{
					chart: {
						toolbar: {
							show: false
						},

					},
					colors: ['#004DCF'],
					stroke: { width: 1, curve: 'smooth' },
					dataLabels: { enabled: false },
					xaxis: {
					    show: false,

					},
					yaxis: {
						show: true,
					}
				}}
			/>
		</div>
	)
}

export default ApexChart
